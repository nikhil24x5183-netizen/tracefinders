"""
TRACE FINDERS — Automated ReportLab PDF Document Generator
Compiles all Markdown documentation files into true A4 PDF binary files (.pdf)
stored in 'pdf_documents/' directory.
"""

import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Preformatted

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(ROOT_DIR, "pdf_documents")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DOC_FILES = [
    "README.md",
    "ARCHITECTURE.md",
    "RESEARCH_NOTES.md",
    "API_SPECIFICATION.md",
    "SECURITY_AND_COMPLIANCE.md",
    "USER_MANUAL.md",
    "DOCUMENTATION_INDEX.md"
]

def clean_text(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # remove md links
    text = text.replace('**', '').replace('__', '').replace('`', '')
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return text.strip()

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=20,
    leading=24,
    textColor=colors.HexColor('#1e3a8a'),
    spaceAfter=12
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=16,
    leading=20,
    textColor=colors.HexColor('#1e3a8a'),
    spaceBefore=14,
    spaceAfter=8
)

h2_style = ParagraphStyle(
    'SectionH2',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=16,
    textColor=colors.HexColor('#2563eb'),
    spaceBefore=10,
    spaceAfter=6
)

body_style = ParagraphStyle(
    'BodyDark',
    parent=styles['BodyText'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#0f172a'),
    spaceAfter=6
)

code_style = ParagraphStyle(
    'CodeSnippet',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=8.5,
    leading=11,
    textColor=colors.HexColor('#38bdf8'),
    backColor=colors.HexColor('#0f172a'),
    spaceBefore=6,
    spaceAfter=6,
    borderPadding=6
)

for doc in DOC_FILES:
    filepath = os.path.join(ROOT_DIR, doc)
    if not os.path.exists(filepath):
        continue

    pdf_filename = doc.replace(".md", ".pdf")
    pdf_filepath = os.path.join(OUTPUT_DIR, pdf_filename)

    doc_pdf = SimpleDocTemplate(
        pdf_filepath,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    story = []
    
    # Header Banner
    story.append(Paragraph(f"TRACE FINDERS (SIH26189) — OFFICIAL DOCUMENTATION PDF: {doc}", ParagraphStyle('HeadBanner', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#64748b'))))
    story.append(Spacer(1, 10))

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_code = False
    code_block = []

    for line in lines:
        raw = line.rstrip()
        if raw.startswith("```"):
            if in_code:
                in_code = False
                code_text = "\n".join(code_block)
                story.append(Preformatted(code_text, code_style))
                code_block = []
            else:
                in_code = True
            continue

        if in_code:
            code_block.append(raw)
            continue

        if not raw:
            story.append(Spacer(1, 4))
            continue

        if raw.startswith("# "):
            story.append(Paragraph(clean_text(raw[2:]), title_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceAfter=8))
        elif raw.startswith("## "):
            story.append(Paragraph(clean_text(raw[3:]), h1_style))
        elif raw.startswith("### "):
            story.append(Paragraph(clean_text(raw[4:]), h2_style))
        elif raw.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=8, spaceAfter=8))
        else:
            story.append(Paragraph(clean_text(raw), body_style))

    doc_pdf.build(story)
    print(f"[PDF CREATED] Generated '{pdf_filename}' ({os.path.getsize(pdf_filepath)} bytes)")

print(f"\n[OK] All {len(DOC_FILES)} PDF files successfully compiled into '{OUTPUT_DIR}'!")
