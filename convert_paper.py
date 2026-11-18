import re
import os
import subprocess
import time
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def make_docx(md_path, docx_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = Document()
    
    # Page Setup: A4, Margins: Top 3cm, Bottom 3cm, Left 4cm, Right 3cm
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.18)    # ~3 cm
    section.bottom_margin = Inches(1.18) # ~3 cm
    section.left_margin = Inches(1.57)   # ~4 cm
    section.right_margin = Inches(1.18)  # ~3 cm

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.35
    normal_style.paragraph_format.space_after = Pt(4)

    i = 0
    in_table = False
    table_lines = []
    in_code = False
    code_lines = []

    def flush_table(tbl_lines):
        if not tbl_lines:
            return
        parsed_rows = []
        for tl in tbl_lines:
            tl = tl.strip()
            if not tl.startswith("|") or not tl.endswith("|"):
                continue
            cells = [c.strip() for c in tl[1:-1].split("|")]
            # skip separator row
            if all(re.match(r"^:?-+:?$", c) for c in cells):
                continue
            parsed_rows.append(cells)
        if not parsed_rows:
            return

        cols_count = max(len(r) for r in parsed_rows)
        table = doc.add_table(rows=len(parsed_rows), cols=cols_count)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, color="B0BEC5", sz="6")

        for r_idx, row_data in enumerate(parsed_rows):
            is_header = (r_idx == 0)
            row = table.rows[r_idx]
            for c_idx in range(cols_count):
                cell = row.cells[c_idx]
                text = row_data[c_idx] if c_idx < len(row_data) else ""
                cell.text = ""
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                
                clean_text = text.replace("**", "").replace("`", "").replace("*", "")
                run = p.add_run(clean_text)
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)

                if is_header:
                    set_cell_background(cell, "2C3E50")
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    if r_idx % 2 == 1:
                        set_cell_background(cell, "F8F9FA")
                    else:
                        set_cell_background(cell, "FFFFFF")
                    if "COCOK" in text or "BERUBAH" in text or "KRITIS" in text or "200" in text:
                        if "COCOK" in text or "MATCH" in text:
                            run.font.bold = True
                            run.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
                        elif "KRITIS" in text or "BERUBAH" in text:
                            run.font.bold = True
                            run.font.color.rgb = RGBColor(0xB7, 0x1C, 0x1C)
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(4)

    while i < len(lines):
        line = lines[i].rstrip("\r\n")

        # Code block handling
        if line.startswith("```"):
            if in_code:
                in_code = False
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.4)
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.line_spacing = 1.0
                run = p.add_run("\n".join(code_lines))
                run.font.name = "Consolas"
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                code_lines = []
            else:
                if in_table:
                    flush_table(table_lines)
                    table_lines = []
                    in_table = False
                in_code = True
                code_lines = []
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Table handling
        if line.strip().startswith("|") and line.strip().endswith("|"):
            in_table = True
            table_lines.append(line)
            i += 1
            continue
        elif in_table:
            flush_table(table_lines)
            table_lines = []
            in_table = False

        # Blank line
        if not line.strip():
            i += 1
            continue

        # Horizontal Rule
        if line.strip() == "---":
            i += 1
            continue

        # Headings
        if line.startswith("# "):
            title_text = line[2:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(title_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(16)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x1A, 0x25, 0x2F)
            i += 1
            continue

        if line.startswith("## "):
            h2_text = line[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(h2_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(13.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
            i += 1
            continue

        if line.startswith("### "):
            h3_text = line[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(h3_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x34, 0x49, 0x5E)
            i += 1
            continue

        # Subtitle or Bold Header
        if line.startswith("**Studi Kasus:"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(14)
            run = p.add_run(line.replace("**", ""))
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
            i += 1
            continue

        # Metadata box / list
        if line.startswith("**Disusun Oleh:**") or line.startswith("- **Nama:") or line.startswith("- **NIM:") or line.startswith("- **Program Studi:") or line.startswith("- **Fakultas") or line.startswith("- **Mata Kuliah:") or line.startswith("- **Tahun"):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.2)
            p.paragraph_format.space_after = Pt(2)
            clean_l = line.replace("- ", "").replace("**", "")
            parts = clean_l.split(":", 1)
            r1 = p.add_run(parts[0] + ":")
            r1.font.bold = True
            r1.font.size = Pt(11)
            if len(parts) > 1:
                r2 = p.add_run(parts[1])
                r2.font.size = Pt(11)
            i += 1
            continue

        # Bullet points
        if line.strip().startswith("- ") or line.strip().startswith("* "):
            bullet_text = line.strip()[2:]
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.3
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            # Parse bold spans
            tokens = re.split(r'(\*\*.*?\*\*)', bullet_text)
            for tok in tokens:
                if tok.startswith("**") and tok.endswith("**"):
                    r = p.add_run(tok[2:-2])
                    r.font.bold = True
                else:
                    sub_tokens = re.split(r'(`.*?`)', tok)
                    for stok in sub_tokens:
                        if stok.startswith("`") and stok.endswith("`"):
                            r = p.add_run(stok[1:-1])
                            r.font.name = "Consolas"
                            r.font.size = Pt(10.5)
                        else:
                            p.add_run(stok)
            i += 1
            continue

        # Numbered list
        m_num = re.match(r"^(\d+)\.\s+(.*)$", line.strip())
        if m_num:
            num = m_num.group(1)
            num_text = m_num.group(2)
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.first_line_indent = Inches(-0.25)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.3
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            p.add_run(f"{num}. ")
            tokens = re.split(r'(\*\*.*?\*\*)', num_text)
            for tok in tokens:
                if tok.startswith("**") and tok.endswith("**"):
                    r = p.add_run(tok[2:-2])
                    r.font.bold = True
                else:
                    p.add_run(tok)
            i += 1
            continue

        # Normal Paragraph
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.35
        
        # Abstract formatting (italicized)
        is_abstract = "ABSTRAK" in line or "ABSTRACT" in line or (i > 0 and ("ABSTRAK" in lines[i-1] or "ABSTRACT" in lines[i-1]))
        tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', line)
        for tok in tokens:
            if tok.startswith("**") and tok.endswith("**"):
                r = p.add_run(tok[2:-2])
                r.font.bold = True
            elif tok.startswith("*") and tok.endswith("*"):
                r = p.add_run(tok[1:-1])
                r.font.italic = True
            elif tok.startswith("`") and tok.endswith("`"):
                r = p.add_run(tok[1:-1])
                r.font.name = "Consolas"
                r.font.size = Pt(10.5)
            else:
                p.add_run(tok)
        i += 1

    if in_table:
        flush_table(table_lines)

    doc.save(docx_path)
    print(f"DOCX created: {docx_path}")

def make_html_and_pdf(md_path, html_path, pdf_path):
    import markdown
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    body_html = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code']
    )

    full_html = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Paper Forensik NIST - PT Satseet International</title>
<style>
  @page {{
    size: A4;
    margin: 30mm 25mm 25mm 30mm;
    @bottom-center {{
      content: counter(page);
      font-family: 'Times New Roman', serif;
      font-size: 10pt;
    }}
  }}
  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.45;
    color: #111;
    background: #fff;
    margin: 0;
    padding: 0;
  }}
  .paper-container {{
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }}
  h1 {{
    font-size: 16pt;
    text-align: center;
    text-transform: uppercase;
    font-weight: bold;
    margin-bottom: 8px;
    color: #1a252f;
  }}
  p strong:first-child {{
    color: #2c3e50;
  }}
  h2 {{
    font-size: 13.5pt;
    font-weight: bold;
    color: #2c3e50;
    border-bottom: 1.5px solid #bdc3c7;
    padding-bottom: 4px;
    margin-top: 24px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 12pt;
    font-weight: bold;
    color: #34495e;
    margin-top: 16px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}
  p {{
    text-align: justify;
    text-justify: inter-word;
    margin-top: 4px;
    margin-bottom: 8px;
  }}
  ul, ol {{
    margin-top: 4px;
    margin-bottom: 8px;
    padding-left: 28px;
    text-align: justify;
  }}
  li {{
    margin-bottom: 4px;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 14px 0;
    font-size: 9.5pt;
    line-height: 1.25;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #bdc3c7;
    padding: 7px 10px;
  }}
  th {{
    background-color: #2c3e50;
    color: #ffffff;
    font-weight: bold;
    text-align: center;
  }}
  tr:nth-child(even) td {{
    background-color: #f8f9fa;
  }}
  pre {{
    background-color: #f4f6f7;
    border: 1px solid #d5dbdb;
    border-left: 4px solid #2980b9;
    padding: 10px 14px;
    font-family: Consolas, 'Courier New', monospace;
    font-size: 9pt;
    overflow-x: auto;
    page-break-inside: avoid;
    line-height: 1.3;
  }}
  code {{
    font-family: Consolas, 'Courier New', monospace;
    font-size: 9.5pt;
    background-color: #eaeded;
    padding: 1px 4px;
    border-radius: 3px;
  }}
  hr {{
    border: none;
    border-top: 1px solid #bdc3c7;
    margin: 18px 0;
  }}
  .meta-box {{
    background: #fdfefe;
    border: 1px solid #d5dbdb;
    border-radius: 4px;
    padding: 10px 16px;
    margin: 12px 0 20px 0;
    font-size: 11pt;
  }}
  @media print {{
    body {{
      padding: 0;
    }}
    .paper-container {{
      max-width: 100%;
      padding: 0;
    }}
  }}
</style>
</head>
<body>
<div class="paper-container">
{body_html}
</div>
</body>
</html>
'''
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"HTML created: {html_path}")

    # Edge headless PDF export
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge_path):
        cmd = [
            edge_path,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        time.sleep(2)
        if os.path.exists(pdf_path):
            print(f"PDF created successfully: {pdf_path} (size: {os.path.getsize(pdf_path)} bytes)")
        else:
            print("Edge failed to create PDF, stderr:", res.stderr)
    else:
        print("Edge not found at standard path.")

if __name__ == "__main__":
    base_dir = r"c:\Users\user\Documents\paket_data_contoh"
    md = os.path.join(base_dir, "PAPER_HASIL_FORENSIK_NIST.md")
    docx = os.path.join(base_dir, "PAPER_HASIL_FORENSIK_NIST.docx")
    html = os.path.join(base_dir, "PAPER_HASIL_FORENSIK_NIST.html")
    pdf = os.path.join(base_dir, "PAPER_HASIL_FORENSIK_NIST.pdf")

    make_docx(md, docx)
    make_html_and_pdf(md, html, pdf)
