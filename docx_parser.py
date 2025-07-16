from docx import Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import Table
from docx.text.paragraph import Paragraph

def iter_block_items(parent):
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def parse_docx(docx_path):
    doc = Document(docx_path)
    elements = []

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            style = block.style.name
            align = block.alignment
            runs = []

            for run in block.runs:
                text = run.text or ""
                for part in text.split('\n'):
                    if part:
                        marks = []
                        if run.bold:
                            marks.append("bold")
                        if run.italic:
                            marks.append("italic")
                        if run.underline:
                            marks.append("underline")

                        style_attrs = {}
                        if run.font.size:
                            style_attrs["fontSize"] = f"{run.font.size.pt}pt"
                        if run.font.name:
                            style_attrs["fontFamily"] = run.font.name
                        if run.font.color and run.font.color.rgb:
                            style_attrs["color"] = f"#{run.font.color.rgb}"

                        if style_attrs:
                            marks.append({"type": "textStyle", "attrs": style_attrs})

                        runs.append({
                            "type": "text",
                            "text": part,
                            "marks": marks
                        })
                    runs.append({"type": "hardBreak"})

            if runs and runs[-1]["type"] == "hardBreak":
                runs.pop()

            elements.append({
                "type": "heading" if style.startswith("Heading") else "paragraph",
                "style": style,
                "alignment": align,
                "content": runs,
                "is_list": style.startswith("List"),
                "list_type": "bullet" if "Bullet" in style else "ordered" if "Number" in style else None
            })

        elif isinstance(block, Table):
            table_data = []
            for row in block.rows:
                row_data = []
                for cell in row.cells:
                    cell_text = "\n".join(p.text for p in cell.paragraphs)
                    row_data.append(cell_text)
                table_data.append(row_data)
            elements.append({
                "type": "table",
                "rows": table_data
            })

    return elements
