#!/usr/bin/env python3
"""PreCompact hook: save session transcript before context compaction.

Reads the session JSONL (path provided via stdin from Claude Code hook system)
and writes a markdown transcript to inputs/conversations/. Only saves messages
added since the last save (tracked via a bookmark file) to avoid duplicates
across multiple compactions in the same session.

Usage (as a Claude Code PreCompact command hook):
  Configured in .claude/settings.json — receives hook JSON on stdin.
  Can also run standalone for testing (falls back to most recent JSONL).
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


BOOKMARK_FILE = "memory/.bookmarks.json"


def get_session_info():
    """Get session ID and JSONL path from stdin (hook) or filesystem (fallback)."""
    # Try reading hook JSON from stdin
    if not sys.stdin.isatty():
        try:
            hook_data = json.load(sys.stdin)
            session_id = hook_data.get("session_id", "")
            transcript_path = hook_data.get("transcript_path", "")
            if transcript_path and Path(transcript_path).exists():
                return session_id, Path(transcript_path)
        except (json.JSONDecodeError, KeyError):
            pass

    # Fallback: find most recently modified .jsonl in Claude project dir
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    encoded = project_dir.replace("/", "-")
    session_dir = Path.home() / ".claude" / "projects" / encoded

    if not session_dir.exists():
        print(f"Session dir not found: {session_dir}", file=sys.stderr)
        return None, None

    jsonl_files = sorted(
        session_dir.glob("*.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not jsonl_files:
        print("No .jsonl files found", file=sys.stderr)
        return None, None

    return jsonl_files[0].stem, jsonl_files[0]


def get_bookmarks_path(project_dir):
    """Resolve the bookmarks file path."""
    return Path(project_dir) / BOOKMARK_FILE


def get_bookmark(project_dir, session_id):
    """Get the last-saved line number for this session. Returns 0 if no bookmark."""
    path = get_bookmarks_path(project_dir)
    if path.exists():
        try:
            data = json.loads(path.read_text())
            return data.get(session_id, 0)
        except (json.JSONDecodeError, OSError):
            return 0
    return 0


def set_bookmark(project_dir, session_id, line_number):
    """Save the last-saved line number for this session."""
    path = get_bookmarks_path(project_dir)
    data = {}
    if path.exists():
        try:
            data = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            data = {}
    data[session_id] = line_number
    path.write_text(json.dumps(data, indent=2) + "\n")


def extract_transcript(jsonl_path, start_line=0):
    """Extract user and assistant text messages from session JSONL.

    Args:
        jsonl_path: Path to the JSONL file.
        start_line: Skip this many lines (already saved in previous compaction).

    Returns:
        (messages, total_lines) — messages is a list of (role, content) tuples.
    """
    messages = []
    total_lines = 0

    with open(jsonl_path) as f:
        for i, line in enumerate(f):
            total_lines = i + 1
            if i < start_line:
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg_type = obj.get("type")

            if msg_type == "user":
                content = obj.get("message", {}).get("content", "")
                if isinstance(content, str) and content.strip():
                    messages.append(("user", content.strip()))
                elif isinstance(content, list):
                    texts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            texts.append(block["text"])
                        elif isinstance(block, str):
                            texts.append(block)
                    if texts:
                        messages.append(("user", "\n".join(texts).strip()))

            elif msg_type == "assistant":
                content = obj.get("message", {}).get("content", [])
                if isinstance(content, list):
                    texts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text = block.get("text", "").strip()
                            if text:
                                texts.append(text)
                    if texts:
                        messages.append(("assistant", "\n\n".join(texts)))
                elif isinstance(content, str) and content.strip():
                    messages.append(("assistant", content.strip()))

    return messages, total_lines


def format_transcript(messages, session_id, part=None):
    """Format messages as markdown transcript."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    date = datetime.now().strftime("%Y-%m-%d")

    title = f"# Session Transcript — {date}"
    if part:
        title += f" (part {part})"

    lines = [
        title,
        "",
        f"Session ID: `{session_id}`",
        f"Saved: {now} (pre-compaction)",
        f"Messages: {len(messages)}",
        "",
        "---",
        "",
    ]

    for role, content in messages:
        if role == "user":
            lines.append("## User")
            lines.append("")
            lines.append(content)
            lines.append("")
        else:
            lines.append("## Assistant")
            lines.append("")
            lines.append(content)
            lines.append("")

    return "\n".join(lines)


def main():
    session_id, jsonl_path = get_session_info()
    if not jsonl_path:
        sys.exit(1)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

    # Read bookmark — how far into the JSONL we've already saved
    start_line = get_bookmark(project_dir, session_id)
    messages, total_lines = extract_transcript(jsonl_path, start_line=start_line)

    if not messages:
        print("No new messages since last save", file=sys.stderr)
        sys.exit(0)

    # Determine part number (1-indexed) for filename
    part = 1 if start_line == 0 else None
    if start_line > 0:
        # Count existing parts for this session
        out_dir = Path(project_dir) / "inputs" / "conversations"
        short_id = session_id[:8] if session_id else "unknown"
        existing = sorted(out_dir.glob(f"pre-compact-*-{short_id}*.md"))
        part = len(existing) + 1

    # Format part suffix for filename
    short_id = session_id[:8] if session_id else "unknown"
    date = datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(project_dir) / "inputs" / "conversations"
    out_dir.mkdir(parents=True, exist_ok=True)

    if part and part > 1:
        out_path = out_dir / f"pre-compact-{date}-{short_id}-part{part}.md"
    else:
        out_path = out_dir / f"pre-compact-{date}-{short_id}.md"

    transcript = format_transcript(messages, session_id, part=part if part and part > 1 else None)

    with open(out_path, "w") as f:
        f.write(transcript)

    # Update bookmark so next compaction only saves new messages
    set_bookmark(project_dir, session_id, total_lines)

    print(f"Saved {len(messages)} new messages to {out_path} (lines {start_line+1}-{total_lines})")


if __name__ == "__main__":
    main()
