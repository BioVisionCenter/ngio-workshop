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
    content = re.sub(r'\s*layout_file\s*=\s*(?:"[^"]*"|\'[^\']*\'),?\n', '\n', py_path.read_text())
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


def inject_notebooks(notebooks: list[dict]) -> None:
    template = (DOCS_DIR / "index.html").read_text()
    cards = "".join(
        f'        <a class="nb-card" href="{nb["href"]}">\n'
        f'          <span class="nb-num">{nb["number"]}</span>\n'
        f'          <span class="nb-title">{nb["title"]}</span>\n'
        f'          <span class="nb-arrow">&#8594;</span>\n'
        f'        </a>\n'
        for nb in notebooks
    )
    start = "<!-- notebooks:start -->"
    end = "<!-- notebooks:end -->"
    updated = re.sub(
        rf"{re.escape(start)}.*?{re.escape(end)}",
        f"{start}\n{cards}        {end}",
        template,
        flags=re.DOTALL,
    )
    (DOCS_DIR / "index.html").write_text(updated)


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

    inject_notebooks(notebooks)
    print(f"Updated docs/index.html with {len(notebooks)} notebook(s)")


if __name__ == "__main__":
    main()
