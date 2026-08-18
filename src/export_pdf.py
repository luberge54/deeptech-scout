"""Turn the Markdown deliverables into print-ready PDFs.

No API call and no new system dependency: the Markdown is rendered to styled HTML
in Python, and Chrome prints it headlessly. Chrome ships on this machine already,
and it keeps hyperlinks live in the output, which matters here - every score in
the market map is backed by source links a reader should be able to click.

Produces one PDF per document plus a combined report, all under pdf/.

Run with:  .venv\\Scripts\\python.exe src\\export_pdf.py
"""

import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import markdown

DOCS_DIR = Path("docs")
OUTPUT_DIR = Path("pdf")

# Chrome is checked in this order; the first that exists is used.
CHROME_CANDIDATES = (
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
)

PRINT_TIMEOUT_SECONDS = 120

# Each entry becomes its own PDF, and all of them become the combined report.
DOCUMENTS = (
    {
        "file": "03-market-map.md",
        "slug": "market-map",
        "title": "The Market Map",
        "blurb": "Five companies scored against five weighted criteria, with every "
        "claim linked to the page it came from.",
    },
    {
        "file": "04-thesis.md",
        "slug": "thesis",
        "title": "The Thesis",
        "blurb": "What the ranking means, the position it supports, and the events "
        "that would show the position is wrong.",
    },
    {
        "file": "00-scoping.md",
        "slug": "method",
        "title": "Method and Limitations",
        "blurb": "The criteria and their weights, fixed before any company was "
        "scored; the calibration against blind hand-scores; and what this cannot see.",
    },
)

REPORT_TITLE = "Physical AI in Switzerland and Europe"
REPORT_SUBTITLE = "An opinionated market map"
AUTHOR = "Lucas Bergerot"

STYLESHEET = """
@page { size: A4; margin: 20mm 18mm; }

html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }

body {
  font-family: Georgia, "Iowan Old Style", serif;
  font-size: 10.5pt;
  line-height: 1.55;
  color: #1a1a1a;
  margin: 0;
}

h1, h2, h3, h4 {
  font-family: "Segoe UI", Helvetica, Arial, sans-serif;
  color: #0f172a;
  line-height: 1.25;
  break-after: avoid;
}

h1 { font-size: 21pt; margin: 0 0 0.6em; letter-spacing: -0.01em; }
h2 {
  font-size: 15pt;
  margin: 1.9em 0 0.7em;
  padding-bottom: 0.3em;
  border-bottom: 1.5px solid #0f172a;
  break-before: page;
}
h3 { font-size: 12.5pt; margin: 1.5em 0 0.5em; color: #1e293b; }
h4 { font-size: 11pt; margin: 1.2em 0 0.4em; color: #334155; }

/* The first heading of a document must not push a blank page in front of it. */
h1 + h2, .doc-start h2:first-of-type { break-before: auto; }

p { margin: 0 0 0.75em; orphans: 3; widows: 3; }

strong { color: #0f172a; }
em { color: #334155; }

a { color: #1d4ed8; text-decoration: none; }

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0 1.4em;
  font-family: "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 8.6pt;
  break-inside: avoid;
}
th {
  background: #0f172a;
  color: #fff;
  text-align: left;
  padding: 6px 8px;
  font-weight: 600;
  vertical-align: bottom;
}
td { padding: 5px 8px; border-bottom: 1px solid #e2e8f0; vertical-align: top; }
tbody tr:nth-child(even) { background: #f8fafc; }

/* Source lists are long and full of URLs. Let them wrap rather than overflow. */
td, li, p { overflow-wrap: anywhere; }

blockquote {
  margin: 1.1em 0;
  padding: 0.5em 0 0.5em 1.1em;
  border-left: 3px solid #0f172a;
  color: #1e293b;
  font-style: italic;
  break-inside: avoid;
}

ul, ol { margin: 0 0 0.9em; padding-left: 1.3em; }
li { margin-bottom: 0.35em; }

code {
  font-family: "Cascadia Mono", Consolas, monospace;
  font-size: 0.88em;
  background: #f1f5f9;
  padding: 1px 4px;
  border-radius: 3px;
}

hr { border: 0; border-top: 1px solid #cbd5e1; margin: 2em 0; }

/* --- cover ------------------------------------------------------------- */
.cover { break-after: page; padding-top: 55mm; }
.cover .eyebrow {
  font-family: "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 9.5pt;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #64748b;
  margin-bottom: 1.2em;
}
.cover h1 { font-size: 30pt; margin-bottom: 0.25em; }
.cover .subtitle {
  font-size: 14pt;
  color: #475569;
  font-style: italic;
  margin-bottom: 2.4em;
}
.cover .rule { width: 60px; border-top: 3px solid #0f172a; margin-bottom: 2.4em; }
.cover .meta {
  font-family: "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 9.5pt;
  color: #475569;
  line-height: 1.8;
}
.cover .meta strong { color: #0f172a; }

/* --- contents ----------------------------------------------------------- */
.contents { break-after: page; }
.contents h2 { break-before: auto; }
.contents ol { list-style: none; padding-left: 0; }
.contents li {
  font-family: "Segoe UI", Helvetica, Arial, sans-serif;
  padding: 0.5em 0;
  border-bottom: 1px solid #e2e8f0;
}
.contents .part-title { font-size: 11.5pt; font-weight: 600; color: #0f172a; }
.contents .part-blurb { font-size: 9pt; color: #64748b; margin-top: 0.2em; }

/* --- part divider ------------------------------------------------------- */
.part { break-before: page; }
.part-label {
  font-family: "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 9pt;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #64748b;
  margin-bottom: 0.4em;
}
"""


def find_browser() -> Path:
    """The first installed Chrome or Edge, which is what prints the PDF."""
    for candidate in CHROME_CANDIDATES:
        if candidate.exists():
            return candidate
    sys.exit(
        "FAIL: no Chrome or Edge found in the usual locations, and one of them is what\n"
        "      turns the HTML into a PDF. Install either, or open the .html files this\n"
        "      script writes and print them with Ctrl+P."
    )


def strip_cross_document_links(text: str) -> str:
    """Turn links between the Markdown files into plain text.

    They resolve on GitHub and are dead in a PDF, and a dead link reads as a
    mistake. The wording around them already names the section.
    """
    return re.sub(r"\[([^\]]+)\]\((?!https?:)[^)]+\)", r"\1", text)


def render_markdown(path: Path) -> str:
    """One document as HTML, with its title line removed - the part page carries it."""
    text = strip_cross_document_links(path.read_text(encoding="utf-8"))
    text = re.sub(r"\A# [^\n]*\n", "", text)
    return markdown.markdown(text, extensions=["tables", "sane_lists"])


def render_cover(title: str, subtitle: str, parts: int) -> str:
    scope = f"{parts} documents" if parts > 1 else "Deliverable"
    return f"""
<section class="cover">
  <div class="eyebrow">Deep-tech market research</div>
  <h1>{title}</h1>
  <div class="subtitle">{subtitle}</div>
  <div class="rule"></div>
  <div class="meta">
    <div><strong>{AUTHOR}</strong></div>
    <div>{date.today().strftime("%d %B %Y")}</div>
    <div>{scope}</div>
  </div>
</section>
"""


def render_contents(documents: tuple) -> str:
    items = "\n".join(
        f'<li><div class="part-title">Part {index}. {doc["title"]}</div>'
        f'<div class="part-blurb">{doc["blurb"]}</div></li>'
        for index, doc in enumerate(documents, start=1)
    )
    return f'<section class="contents"><h2>Contents</h2><ol>{items}</ol></section>'


def build_html(title: str, subtitle: str, documents: tuple, with_contents: bool) -> str:
    """Assemble the printable page for one or more documents."""
    body = [render_cover(title, subtitle, len(documents))]

    if with_contents:
        body.append(render_contents(documents))

    for index, doc in enumerate(documents, start=1):
        opening = ""
        if with_contents:
            opening = (
                f'<div class="part-label">Part {index}</div>'
                f'<h1>{doc["title"]}</h1>'
            )
        body.append(
            f'<section class="part doc-start">{opening}'
            f'{render_markdown(DOCS_DIR / doc["file"])}</section>'
        )

    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{title}</title><style>{STYLESHEET}</style></head>"
        f"<body>{''.join(body)}</body></html>"
    )


def print_to_pdf(browser: Path, html_path: Path, pdf_path: Path) -> None:
    """Drive the browser headlessly. Raises if it produces nothing."""
    profile = OUTPUT_DIR / ".chrome-profile"
    result = subprocess.run(
        [
            str(browser),
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            f"--user-data-dir={profile.resolve()}",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path.resolve()}",
            html_path.resolve().as_uri(),
        ],
        capture_output=True,
        text=True,
        timeout=PRINT_TIMEOUT_SECONDS,
    )

    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        sys.exit(
            f"FAIL: {browser.name} produced no PDF for {html_path.name}.\n"
            f"      {result.stderr.strip()[:400]}"
        )


def export(browser: Path, name: str, title: str, subtitle: str, documents: tuple,
           with_contents: bool) -> Path:
    html_path = OUTPUT_DIR / f"{name}.html"
    pdf_path = OUTPUT_DIR / f"{name}.pdf"

    html_path.write_text(
        build_html(title, subtitle, documents, with_contents), encoding="utf-8"
    )
    print_to_pdf(browser, html_path, pdf_path)

    size_kb = pdf_path.stat().st_size / 1024
    print(f"    {pdf_path}  ({size_kb:,.0f} KB)")
    return pdf_path


def main() -> None:
    missing = [doc["file"] for doc in DOCUMENTS if not (DOCS_DIR / doc["file"]).exists()]
    if missing:
        sys.exit(f"FAIL: missing source document(s): {', '.join(missing)}")

    browser = find_browser()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Exporting {len(DOCUMENTS)} documents with {browser.name}, no API call.\n")

    export(
        browser,
        "DeepTech-Scout-Full-Report",
        REPORT_TITLE,
        REPORT_SUBTITLE,
        DOCUMENTS,
        with_contents=True,
    )

    for doc in DOCUMENTS:
        export(
            browser,
            f"DeepTech-Scout-{doc['slug'].title()}",
            doc["title"],
            REPORT_TITLE,
            (doc,),
            with_contents=False,
        )

    shutil.rmtree(OUTPUT_DIR / ".chrome-profile", ignore_errors=True)
    for leftover in OUTPUT_DIR.glob("*.html"):
        leftover.unlink()

    print(f"\nDone. {len(DOCUMENTS) + 1} PDFs in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
