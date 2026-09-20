from PyPDF2 import PdfReader
from resume_sections import section_for_heading


def _layout_text(page):
    """Extract positioned text in visual order, including simple two-column CVs."""
    fragments = []

    def collect(value, _cm, tm, _font, _size):
        value = value.strip()
        # PyPDF2 sometimes emits an aggregate duplicate containing newlines.
        if value and "\n" not in value:
            fragments.append((float(tm[4]), float(tm[5]), value))

    page.extract_text(visitor_text=collect)
    if not fragments:
        return page.extract_text() or ""

    # A large horizontal gap is a reliable indicator of independent columns.
    positions = sorted({round(x) for x, _, _ in fragments})
    gaps = [(right - left, (left + right) / 2) for left, right in zip(positions, positions[1:])]
    split = max(gaps, default=(0, 0))
    columns = [fragments] if split[0] < 120 else [
        [item for item in fragments if item[0] < split[1]],
        [item for item in fragments if item[0] >= split[1]],
    ]
    lines = []
    for column in columns:
        rows = []
        for x, y, value in sorted(column, key=lambda item: (-item[1], item[0])):
            if rows and abs(rows[-1][0] - y) <= 3:
                rows[-1][1].append((x, value))
            else:
                rows.append([y, [(x, value)]])
        lines.extend(" ".join(value for _, value in sorted(values)) for _, values in rows)
    return "\n".join(line for line in lines if line.strip())


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        plain_text = page.extract_text() or ""
        layout_text = _layout_text(page)
        # Coordinate callbacks are valuable for genuinely positioned PDFs, but
        # some generators expose transformed glyph coordinates inconsistently.
        # Never accept that result when it loses the document's heading structure.
        plain_headings = sum(bool(section_for_heading(line.strip())) for line in plain_text.splitlines())
        layout_headings = sum(bool(section_for_heading(line.strip())) for line in layout_text.splitlines())
        page_text = layout_text if layout_headings >= plain_headings and layout_headings else plain_text

        if page_text:
            text += page_text + "\n"

    return text
