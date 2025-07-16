from docx_parser import parse_docx
from prosemirror_builder import build_prosemirror_json
import json
 
def convert_docx_to_prosemirror(docx_path, output_path):
    elements = parse_docx(docx_path)
    prosemirror_json = build_prosemirror_json(elements)
 
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(prosemirror_json, f, ensure_ascii=False, indent=2)
 
if __name__ == "__main__":
    convert_docx_to_prosemirror("document.docx", "output_prosemirror.json"
