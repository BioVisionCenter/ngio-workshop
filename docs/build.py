# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Build script for ngio-workshop documentation site.

Exports all numbered notebooks to HTML and generates docs/index.html.

Usage:
    uv run docs/build.py
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
NOTEBOOKS_DIR = ROOT / "notebooks"
DOCS_DIR = ROOT / "docs"


def extract_title(py_path: Path) -> str:
    text = py_path.read_text()
    m = re.search(r'mo\.md\(r?f?""".*?#\s+(.+?)\n', text, re.DOTALL)
    if m:
        return m.group(1).strip()
    name = re.sub(r"^\d+_", "", py_path.stem)
    return name.replace("_", " ").title()


def export_notebook(py_path: Path, out_html: Path) -> bool:
    # Strip layout_file before export — marimo inlines it as a data URI on every
    # save, which then breaks inline_layout_file() during export (it tries to
    # open the data URI string as a file path).
    content = re.sub(r'\s*layout_file\s*=\s*[^\n,]+,?\n', '\n', py_path.read_text())
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", dir=py_path.parent, delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)
    try:
        result = subprocess.run(
            ["uvx", "marimo", "export", "html", "--sandbox", str(tmp_path), "-o", str(out_html)],
            capture_output=True,
            text=True,
        )
    finally:
        tmp_path.unlink(missing_ok=True)
    if result.returncode != 0:
        print(f"  ERROR: {py_path.name}\n{result.stderr}", file=sys.stderr)
        return False
    return True


def build_index(notebooks: list[dict]) -> str:
    cards = "".join(
        f"""      <a class="nb-card" href="{nb['href']}">
        <span class="nb-num">{nb['number']}</span>
        <span class="nb-title">{nb['title']}</span>
        <span class="nb-arrow">&#8594;</span>
      </a>\n"""
        for nb in notebooks
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ngio Workshop</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: system-ui, -apple-system, sans-serif; background: #f8f9fb; color: #1a1a2e; min-height: 100vh; }}

    header {{
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
      color: white;
      padding: 3.5rem 2rem 3rem;
    }}
    .header-inner {{ max-width: 720px; margin: 0 auto; }}
    .badge {{
      display: inline-block; font-size: 0.7rem; font-weight: 700;
      letter-spacing: 0.1em; text-transform: uppercase;
      color: #7dd3fc; margin-bottom: 1rem;
    }}
    h1 {{ font-size: 2.25rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 0.75rem; }}
    .subtitle {{ font-size: 1rem; color: #94a3b8; line-height: 1.65; max-width: 500px; }}
    .subtitle a {{ color: #7dd3fc; text-decoration: none; }}
    .subtitle a:hover {{ text-decoration: underline; }}

    main {{ max-width: 720px; margin: 0 auto; padding: 2.5rem 2rem; }}

    .section-label {{
      font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em;
      text-transform: uppercase; color: #64748b; margin-bottom: 1rem;
    }}

    .nb-list {{ display: flex; flex-direction: column; gap: 0.6rem; }}

    .nb-card {{
      display: flex; align-items: center; gap: 1.1rem;
      background: white; border: 1px solid #e2e8f0; border-radius: 10px;
      padding: 1.1rem 1.4rem; text-decoration: none; color: inherit;
      transition: border-color 0.15s, box-shadow 0.15s, transform 0.1s;
    }}
    .nb-card:hover {{
      border-color: #7dd3fc;
      box-shadow: 0 4px 16px rgba(125, 211, 252, 0.15);
      transform: translateY(-1px);
    }}

    .nb-num {{
      flex-shrink: 0; width: 2rem; height: 2rem;
      background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 6px;
      display: flex; align-items: center; justify-content: center;
      font-size: 0.85rem; font-weight: 700; color: #0369a1;
    }}
    .nb-title {{ font-size: 0.975rem; font-weight: 600; color: #1a1a2e; }}
    .nb-arrow {{
      margin-left: auto; color: #94a3b8; font-size: 1rem;
      transition: color 0.15s, transform 0.15s;
    }}
    .nb-card:hover .nb-arrow {{ color: #0369a1; transform: translateX(3px); }}

    footer {{
      max-width: 720px; margin: 0 auto; padding: 0 2rem 3rem;
      font-size: 0.82rem; color: #94a3b8;
    }}
    footer a {{ color: #64748b; text-decoration: none; }}
    footer a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <header>
    <div class="header-inner">
      <div class="badge">Workshop</div>
      <h1>ngio Workshop</h1>
      <p class="subtitle">
        Hands-on notebooks for <a href="https://github.com/fractal-analytics-platform/ngio">ngio</a>,
        a Python library for reading and writing OME-Zarr bioimages.
      </p>
    </div>
  </header>

  <main>
    <div class="section-label">Notebooks</div>
    <div class="nb-list">
{cards}    </div>
  </main>

  <footer>
    Built with <a href="https://marimo.io">marimo</a> &amp;
    <a href="https://docs.astral.sh/uv/">uv</a>.
  </footer>
</body>
</html>
"""


def main():
    DOCS_DIR.mkdir(exist_ok=True)

    py_files = sorted(
        p for p in NOTEBOOKS_DIR.glob("*.py")
        if re.match(r"^\d+_", p.name) and not p.stem.endswith("_old")
    )

    if not py_files:
        print("No numbered notebooks found.", file=sys.stderr)
        sys.exit(1)

    notebooks = []
    for py_path in py_files:
        out_html = DOCS_DIR / f"{py_path.stem}.html"
        title = extract_title(py_path)
        print(f"Exporting {py_path.name} -> docs/{py_path.stem}.html")
        m = re.match(r"^(\d+)_", py_path.name)
        number = m.group(1) if m else "?"
        if export_notebook(py_path, out_html):
            notebooks.append({"href": f"{py_path.stem}.html", "title": title, "number": number})

    (DOCS_DIR / "index.html").write_text(build_index(notebooks))
    print(f"Generated docs/index.html with {len(notebooks)} notebook(s)")


if __name__ == "__main__":
    main()
