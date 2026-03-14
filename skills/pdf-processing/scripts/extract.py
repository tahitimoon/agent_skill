import sys
import json
from pathlib import Path

import pymupdf


def extract_text(pdf_path: str) -> dict:
    """提取 PDF 文本内容"""
    try:
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            return {"success": False, "error": f"File not found: {pdf_path}"}

        text_content = []
        pdf_document = pymupdf.open(pdf_path)

        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            page_text = page.get_text("text")
            if page_text.strip():
                text_content.append({"page": page_num + 1, "text": page_text})

        pdf_document.close()

        return {
            "success": True,
            "total_pages": len(text_content),
            "content": text_content,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    pdf_path = sys.argv[1]
    result = extract_text(pdf_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
