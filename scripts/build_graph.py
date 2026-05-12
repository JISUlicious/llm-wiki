"""Build a self-contained force-directed graph of the wiki.

Scans wiki/{entities,concepts,sources,comparisons,queries}/*.md, extracts
frontmatter metadata and [[wikilinks]], and writes wiki/graph.html — a single
HTML file using d3.js (loaded from CDN) with the graph data embedded inline.

Usage:
    python scripts/build_graph.py
    open wiki/graph.html
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
OUTPUT = REPO_ROOT / "graph.html"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+?)(?:[|#][^\]]*)?\]\]")
TITLE_RE = re.compile(r"^title:\s*['\"]?(.*?)['\"]?\s*$", re.MULTILINE)
TYPE_RE = re.compile(r"^type:\s*(\w+)", re.MULTILINE)


def slug(filename: str) -> str:
    return Path(filename).stem.lower()


def parse_page(path: Path) -> dict:
    text = path.read_text()
    fm_match = FRONTMATTER_RE.match(text)
    fm = fm_match.group(1) if fm_match else ""
    body = text[fm_match.end():] if fm_match else text

    title_m = TITLE_RE.search(fm)
    type_m = TYPE_RE.search(fm)

    links = []
    for m in WIKILINK_RE.finditer(body):
        target = slug(m.group(1).strip())
        if target and target not in links:
            links.append(target)

    return {
        "id": slug(path.name),
        "title": title_m.group(1).strip() if title_m else path.stem,
        "type": (type_m.group(1).strip() if type_m else "unknown"),
        "category": path.parent.name,
        "links": links,
        "path": str(path.relative_to(WIKI_DIR.parent)),
        "body": body.lstrip("\n"),
    }


def build_graph():
    pages = []
    for category in ["entities", "concepts", "sources", "comparisons", "queries"]:
        cdir = WIKI_DIR / category
        if not cdir.is_dir():
            continue
        for md in sorted(cdir.glob("*.md")):
            pages.append(parse_page(md))

    node_ids = {p["id"] for p in pages}
    nodes = [{
        "id": p["id"],
        "title": p["title"],
        "type": p["type"],
        "category": p["category"],
        "path": p["path"],
        "body": p["body"],
    } for p in pages]

    edges = []
    for p in pages:
        for target in p["links"]:
            if target in node_ids:
                edges.append({"source": p["id"], "target": target})

    # Count missing-page targets (links to pages that don't exist) — useful
    # for users to see gaps in the wiki.
    missing = {}
    for p in pages:
        for target in p["links"]:
            if target not in node_ids:
                missing[target] = missing.get(target, 0) + 1

    return {"nodes": nodes, "edges": edges, "missing": missing}


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Wiki Graph</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    html, body { margin: 0; padding: 0; height: 100%; font-family: -apple-system, system-ui, sans-serif; background: #fafafa; }
    #toolbar { position: fixed; top: 12px; left: 12px; z-index: 10; background: rgba(255,255,255,0.95); border: 1px solid #ddd; border-radius: 6px; padding: 10px 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); font-size: 13px; max-width: 280px; }
    #toolbar h3 { margin: 0 0 8px 0; font-size: 14px; }
    #toolbar .legend { display: flex; flex-direction: column; gap: 4px; }
    #toolbar .legend-item { display: flex; align-items: center; gap: 8px; cursor: pointer; user-select: none; }
    #toolbar .legend-item.disabled { opacity: 0.3; }
    #toolbar .swatch { width: 14px; height: 14px; border-radius: 50%; flex-shrink: 0; }
    #toolbar .stats { margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee; color: #666; font-size: 12px; }
    #toolbar input[type=text] { width: 100%; padding: 4px 6px; margin-top: 4px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; font-size: 12px; }
    #panel { position: fixed; top: 0; right: 0; width: 420px; height: 100vh; z-index: 20; background: #fff; border-left: 1px solid #ddd; box-shadow: -2px 0 12px rgba(0,0,0,0.08); display: none; flex-direction: column; }
    #panel.open { display: flex; }
    #panel-header { padding: 14px 18px 10px 18px; border-bottom: 1px solid #eee; flex-shrink: 0; }
    #panel-header h2 { margin: 0; font-size: 16px; line-height: 1.3; padding-right: 28px; }
    #panel-header .meta { color: #888; font-size: 12px; margin-top: 4px; }
    #panel-header a { color: #0366d6; text-decoration: none; }
    #panel-header a:hover { text-decoration: underline; }
    #panel-close { position: absolute; top: 10px; right: 12px; cursor: pointer; background: none; border: none; font-size: 18px; color: #888; line-height: 1; padding: 4px 6px; }
    #panel-close:hover { color: #333; }
    #panel-body { padding: 14px 18px 30px 18px; overflow-y: auto; flex: 1; font-size: 14px; line-height: 1.55; color: #2a2a2a; }
    #panel-body h1 { font-size: 18px; margin-top: 18px; }
    #panel-body h2 { font-size: 16px; margin-top: 16px; border-bottom: 1px solid #eee; padding-bottom: 4px; }
    #panel-body h3 { font-size: 14px; margin-top: 14px; }
    #panel-body code { background: #f4f4f4; padding: 1px 5px; border-radius: 3px; font-size: 12.5px; }
    #panel-body pre { background: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto; }
    #panel-body pre code { background: transparent; padding: 0; }
    #panel-body blockquote { border-left: 3px solid #ddd; margin-left: 0; padding-left: 12px; color: #666; }
    #panel-body table { border-collapse: collapse; font-size: 13px; }
    #panel-body th, #panel-body td { border: 1px solid #ddd; padding: 4px 8px; }
    #panel-body img { max-width: 100%; }
    .wikilink { color: #0366d6; cursor: pointer; text-decoration: none; border-bottom: 1px dashed #b8d4ff; }
    .wikilink:hover { background: #eaf3ff; }
    .wikilink.broken { color: #999; cursor: not-allowed; border-bottom-style: dotted; }
    .wikilink.broken:hover { background: transparent; }
    svg { width: 100vw; height: 100vh; display: block; }
    .node circle { stroke: #fff; stroke-width: 1.5px; cursor: pointer; }
    .node text { font-size: 11px; pointer-events: none; fill: #333; }
    .node.dimmed circle { opacity: 0.2; }
    .node.dimmed text { opacity: 0.2; }
    .link { stroke: #999; stroke-opacity: 0.3; stroke-width: 1px; }
    .link.dimmed { opacity: 0.1; }
    .link.highlighted { stroke: #ff7043; stroke-opacity: 0.9; stroke-width: 2px; }
  </style>
</head>
<body>
  <div id="toolbar">
    <h3>Wiki Graph</h3>
    <input type="text" id="search" placeholder="Filter by title…" />
    <div class="legend" id="legend"></div>
    <div class="stats" id="stats"></div>
  </div>
  <div id="panel">
    <div id="panel-header">
      <button id="panel-close" title="Close">×</button>
      <h2 id="panel-title"></h2>
      <div class="meta" id="panel-meta"></div>
    </div>
    <div id="panel-body"></div>
  </div>
  <svg></svg>

  <script>
  const DATA = __DATA__;

  const TYPE_COLORS = {
    entity: "#5b8def",
    concept: "#7bc97e",
    source: "#f0b35e",
    comparison: "#d672c9",
    query: "#888888",
    unknown: "#bbbbbb",
  };

  const svg = d3.select("svg");
  const width = window.innerWidth;
  const height = window.innerHeight;

  const g = svg.append("g");

  svg.call(d3.zoom().scaleExtent([0.2, 4]).on("zoom", (event) => {
    g.attr("transform", event.transform);
  }));

  const simulation = d3.forceSimulation(DATA.nodes)
    .force("link", d3.forceLink(DATA.edges).id(d => d.id).distance(80).strength(0.6))
    .force("charge", d3.forceManyBody().strength(-180))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collide", d3.forceCollide().radius(20));

  const link = g.append("g").selectAll("line")
    .data(DATA.edges).enter().append("line")
    .attr("class", "link");

  const node = g.append("g").selectAll("g")
    .data(DATA.nodes).enter().append("g")
    .attr("class", "node");

  node.append("circle")
    .attr("r", d => 4 + Math.sqrt(degree(d.id)) * 2)
    .attr("fill", d => TYPE_COLORS[d.type] || TYPE_COLORS.unknown)
    .on("mouseover", (event, d) => highlight(d))
    .on("mouseout", () => unhighlight())
    .on("click", (event, d) => showInfo(d));

  node.append("text")
    .attr("dx", 10).attr("dy", 4)
    .text(d => d.title);

  node.call(d3.drag()
    .on("start", (event, d) => { if (!event.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on("drag", (event, d) => { d.fx = event.x; d.fy = event.y; })
    .on("end", (event, d) => { if (!event.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }));

  simulation.on("tick", () => {
    link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    node.attr("transform", d => `translate(${d.x},${d.y})`);
  });

  function degree(id) {
    return DATA.edges.filter(e => (e.source.id || e.source) === id || (e.target.id || e.target) === id).length;
  }

  function highlight(d) {
    const neighbors = new Set([d.id]);
    DATA.edges.forEach(e => {
      const s = e.source.id || e.source, t = e.target.id || e.target;
      if (s === d.id) neighbors.add(t);
      if (t === d.id) neighbors.add(s);
    });
    node.classed("dimmed", n => !neighbors.has(n.id));
    link.classed("dimmed", e => {
      const s = e.source.id || e.source, t = e.target.id || e.target;
      return !(s === d.id || t === d.id);
    });
    link.classed("highlighted", e => {
      const s = e.source.id || e.source, t = e.target.id || e.target;
      return s === d.id || t === d.id;
    });
  }

  function unhighlight() {
    node.classed("dimmed", false);
    link.classed("dimmed", false).classed("highlighted", false);
  }

  const NODE_BY_ID = Object.fromEntries(DATA.nodes.map(n => [n.id, n]));

  function slugLink(s) {
    // Match Python's slug() behavior for wikilink targets
    return s.split(/[\\/]/).pop().replace(/\.md$/i, "").toLowerCase();
  }

  function rewriteWikilinks(md) {
    // Replace [[target]] or [[target|label]] with anchor tags that route to nodes
    return md.replace(/\[\[([^\]|#]+?)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]/g, (match, target, label) => {
      const id = slugLink(target.trim());
      const display = (label || target).trim();
      if (NODE_BY_ID[id]) {
        return `<a class="wikilink" data-target="${id}">${display}</a>`;
      }
      return `<span class="wikilink broken" title="page not yet created">${display}</span>`;
    });
  }

  function showInfo(d) {
    const inDeg = DATA.edges.filter(e => (e.target.id || e.target) === d.id).length;
    const outDeg = DATA.edges.filter(e => (e.source.id || e.source) === d.id).length;
    const panel = document.getElementById("panel");
    document.getElementById("panel-title").textContent = d.title;
    document.getElementById("panel-meta").innerHTML =
      `${d.type} · ${d.category} · in ${inDeg} / out ${outDeg} · ` +
      `<a href="./${d.path}" target="_blank">${d.path}</a>`;
    const rewritten = rewriteWikilinks(d.body || "*(no content)*");
    document.getElementById("panel-body").innerHTML = marked.parse(rewritten);
    panel.classList.add("open");
    // Wire wikilinks to switch panels
    panel.querySelectorAll(".wikilink[data-target]").forEach(a => {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        const target = NODE_BY_ID[a.dataset.target];
        if (target) {
          showInfo(target);
          // Briefly highlight in the graph
          highlight(target);
          setTimeout(unhighlight, 1500);
        }
      });
    });
  }

  document.getElementById("panel-close").addEventListener("click", () => {
    document.getElementById("panel").classList.remove("open");
  });

  // Type filter legend
  const types = [...new Set(DATA.nodes.map(n => n.type))].sort();
  const enabled = new Set(types);
  const legendEl = document.getElementById("legend");
  types.forEach(t => {
    const counts = DATA.nodes.filter(n => n.type === t).length;
    const div = document.createElement("div");
    div.className = "legend-item";
    div.innerHTML = `<div class="swatch" style="background:${TYPE_COLORS[t] || TYPE_COLORS.unknown}"></div><span>${t} (${counts})</span>`;
    div.onclick = () => {
      if (enabled.has(t)) { enabled.delete(t); div.classList.add("disabled"); }
      else { enabled.add(t); div.classList.remove("disabled"); }
      applyFilters();
    };
    legendEl.appendChild(div);
  });

  // Search
  document.getElementById("search").addEventListener("input", () => applyFilters());

  function applyFilters() {
    const q = document.getElementById("search").value.toLowerCase();
    node.style("display", d => {
      if (!enabled.has(d.type)) return "none";
      if (q && !d.title.toLowerCase().includes(q) && !d.id.includes(q)) return "none";
      return null;
    });
    const visible = new Set(DATA.nodes.filter(d => enabled.has(d.type) && (!q || d.title.toLowerCase().includes(q) || d.id.includes(q))).map(d => d.id));
    link.style("display", e => {
      const s = e.source.id || e.source, t = e.target.id || e.target;
      return visible.has(s) && visible.has(t) ? null : "none";
    });
  }

  document.getElementById("stats").textContent =
    `${DATA.nodes.length} nodes · ${DATA.edges.length} edges` +
    (Object.keys(DATA.missing).length ? ` · ${Object.keys(DATA.missing).length} missing pages referenced` : "");
  </script>
</body>
</html>
"""


def main():
    graph = build_graph()
    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(graph))
    OUTPUT.write_text(html)
    print(f"[graph] {len(graph['nodes'])} nodes, {len(graph['edges'])} edges → {OUTPUT.relative_to(REPO_ROOT)}")
    if graph["missing"]:
        print(f"[graph] {len(graph['missing'])} referenced pages don't exist yet:")
        for name, count in sorted(graph["missing"].items(), key=lambda x: -x[1])[:10]:
            print(f"   - {name} ({count} ref{'s' if count > 1 else ''})")


if __name__ == "__main__":
    main()
