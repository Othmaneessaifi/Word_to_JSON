def build_prosemirror_json(elements):
    def get_alignment(align):
        return {
            0: "left",
            1: "center",
            2: "right",
            3: "justify"
        }.get(align, "left")

    doc = {
        "type": "doc",
        "content": [
            {
                "type": "page",
                "attrs": {
                    "paperSize": "A4",
                    "paperColour": "#fff",
                    "paperOrientation": "portrait",
                    "pageBorders": {"top": 0, "right": 0, "bottom": 0, "left": 0}
                },
                "content": [
                    {
                        "type": "body",
                        "attrs": {
                            "pageMargins": {"top": 25.4, "right": 25.4, "bottom": 25.4, "left": 25.4}
                        },
                        "content": []
                    }
                ]
            }
        ]
    }

    body = doc["content"][0]["content"][0]["content"]
    current_list = None

    for el in elements:
        if el["type"] == "table":
            table_node = {
                "type": "table",
                "content": []
            }
            for row in el["rows"]:
                row_node = {
                    "type": "tableRow",
                    "content": []
                }
                for cell in row:
                    row_node["content"].append({
                        "type": "tableCell",
                        "content": [{
                            "type": "paragraph",
                            "attrs": {"lineHeight": "normal", "textAlign": "left", "margin": None},
                            "content": [{"type": "text", "text": cell}]
                        }]
                    })
                table_node["content"].append(row_node)
            body.append(table_node)
            continue

        content = []
        for run in el["content"]:
            if run["type"] == "hardBreak":
                content.append({"type": "hardBreak"})
            else:
                node = {
                    "type": "text",
                    "text": run["text"]
                }
                if run.get("marks"):
                    node["marks"] = run["marks"]
                content.append(node)

        node = {
            "type": el["type"],
            "attrs": {
                "lineHeight": "100%",
                "textAlign": get_alignment(el["alignment"]),
                "level": int(el["style"].replace("Heading", "").strip()) if el["type"] == "heading" else None,
                "margin": None
            },
            "content": content
        }

        if el.get("is_list"):
            list_type = "bulletList" if el["list_type"] == "bullet" else "orderedList"
            if not current_list or current_list["type"] != list_type:
                current_list = {
                    "type": list_type,
                    "content": []
                }
                body.append(current_list)
            current_list["content"].append({
                "type": "listItem",
                "content": [node]
            })
        else:
            current_list = None
            body.append(node)

    return doc
