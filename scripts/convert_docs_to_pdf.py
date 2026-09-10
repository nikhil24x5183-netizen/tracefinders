"""
TRACE FINDERS — Offline Documentation to HTML/PDF Converter Script
Converts all project markdown documentation files into printable A4 HTML/PDF files
ready to upload directly to Google Drive.
"""

import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(ROOT_DIR, "docs_pdf_export")

DOC_FILES = [
    "README.md",
    "ARCHITECTURE.md",
    "RESEARCH_NOTES.md",
    "API_SPECIFICATION.md",
    "SECURITY_AND_COMPLIANCE.md",
    "USER_MANUAL.md",
    "DOCUMENTATION_INDEX.md"
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

for doc in DOC_FILES:
    filepath = os.path.join(ROOT_DIR, doc)
    if not os.path.exists(filepath):
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content_md = f.read()

    lines = content_md.split("\n")
    html_lines = []
    in_code = False

    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            html_lines.append("<pre><code>" if in_code else "</code></pre>")
            continue
        if in_code:
            html_lines.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            continue
        
        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("#### "):
            html_lines.append(f"<h4>{line[5:]}</h4>")
        elif line.startswith("- "):
            html_lines.append(f"<li>{line[2:]}</li>")
        elif line.startswith("|"):
            html_lines.append(f"<div style='font-family: monospace; font-size: 11px; padding: 4px 0;'>{line}</div>")
        elif line.strip() == "---":
            html_lines.append("<hr>")
        else:
            html_lines.append(f"<p>{line}</p>" if line.strip() else "<br>")

    rendered_body = "\n".join(html_lines)
    out_filename = doc.replace(".md", ".html")
    out_filepath = os.path.join(OUTPUT_DIR, out_filename)

    html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TRACE FINDERS — {doc} (Printable A4 PDF)</title>
    <style>
        @page {{ size: A4; margin: 15mm; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #0f172a;
            background: #ffffff;
            line-height: 1.6;
            font-size: 13px;
            padding: 24px;
            max-width: 840px;
            margin: 0 auto;
        }}
        h1 {{ font-size: 24px; color: #1e3a8a; border-bottom: 2px solid #2563eb; padding-bottom: 8px; margin-top: 20px; }}
        h2 {{ font-size: 18px; color: #1e3a8a; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; margin-top: 18px; }}
        h3 {{ font-size: 15px; color: #2563eb; margin-top: 14px; }}
        code, pre {{ font-family: 'Fira Code', monospace; background: #f8fafc; border: 1px solid #e2e8f0; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
        pre {{ padding: 12px; overflow-x: auto; background: #0f172a; color: #38bdf8; border-radius: 8px; }}
        hr {{ border: 0; border-top: 1px solid #cbd5e1; margin: 20px 0; }}
        li {{ margin-left: 20px; }}
        .no-print {{
            position: fixed;
            top: 16px;
            right: 16px;
            background: #2563eb;
            color: #ffffff;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 800;
            font-size: 13px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            border: none;
            z-index: 1000;
        }}
        @media print {{
            .no-print {{ display: none; }}
            body {{ padding: 0; }}
        }}
    </style>
</head>
<body>
    <button class="no-print" onclick="window.print()">🖨️ Save as A4 PDF</button>
    <div style="font-size: 11px; color: #64748b; font-weight: 800; font-family: monospace; text-transform: uppercase; margin-bottom: 12px;">
        OFFICIAL DOCUMENTATION EXPORT // TRACE FINDERS (SIH26189) // {doc}
    </div>
    {rendered_body}
</body>
</html>"""

    with open(out_filepath, "w", encoding="utf-8") as out_f:
        out_f.write(html_out)

print(f"[OK] Successfully exported printable HTML/PDF files for all 7 documentation files to '{OUTPUT_DIR}'!")
