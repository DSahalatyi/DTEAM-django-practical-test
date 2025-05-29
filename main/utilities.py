import io
from xhtml2pdf import pisa


def html_to_pdf(html: str) -> bytes | None:
    output = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("utf-8")), output)
    if not pdf.err:
        return output.getvalue()
    return None
