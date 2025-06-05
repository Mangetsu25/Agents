import json
from typing import Dict
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def json_to_pdf(data: Dict, path: str) -> None:
    """Generate a PDF file from a JSON-compatible dictionary."""
    c = canvas.Canvas(path, pagesize=letter)
    textobject = c.beginText(40, 750)
    for key, value in data.items():
        line = f"{key}: {json.dumps(value)}"
        textobject.textLine(line)
    c.drawText(textobject)
    c.save()


__all__ = ["json_to_pdf"]
