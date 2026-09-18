from zipfile import ZipFile

import pytest
from reportlab.pdfgen import canvas

from app import app


COMPLETE_RESUME = """Fictional Candidate
fictional.candidate@example.com | 555-010-1234
linkedin.com/in/fictional-candidate | github.com/fictional-candidate

SUMMARY
Backend developer focused on reliable web and data systems.

SKILLS
Python, JavaScript, TypeScript, Flask, React, SQL, PostgreSQL, AWS, Docker, Git

EXPERIENCE
Experience
Python Developer Intern at Example Labs
Software Engineer at Example Systems
Implemented APIs, improved response time by 30%, and optimized automation.

PROJECTS
Projects
Resume Search project: Flask, React, PostgreSQL, Docker, and machine learning.
Sensor project: Python, TensorFlow, and IoT with 100+ users.

EDUCATION
B.Tech in Computer Science, Fictional University, CGPA 8.5

CERTIFICATIONS
AWS Certified Developer, Docker Certification

ACHIEVEMENTS
Increased test coverage by 40%; reduced processing time by 2 seconds.

LANGUAGES
Python, JavaScript, English
"""

MINIMAL_RESUME = """Fictional Candidate
minimal@example.com
Skills
Python
"""

MATCHING_RESUME = """Fictional Match Candidate
Python developer with Python, Flask, SQL, PostgreSQL, AWS, Docker, Git, and machine learning experience.
Projects: Flask API and Python data service.
"""

MISMATCH_RESUME = """Fictional Mismatch Candidate
Graphic designer with illustration, typography, and print layout experience.
Projects: poster design and brand identity project.
"""

JOB_DESCRIPTION = """Looking for a Python backend engineer with Flask, SQL, PostgreSQL, AWS,
Docker, Git, and machine learning experience."""


def _write_pdf(path, text):
    document = canvas.Canvas(str(path))
    document.setTitle("Fictional Resume Fixture")
    y = 800
    for line in text.splitlines():
        document.drawString(40, y, line[:110])
        y -= 14
        if y < 40:
            document.showPage()
            y = 800
    document.save()


def _write_docx(path, text):
    document_xml = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">',
        "<w:body>",
    ]
    for line in text.splitlines():
        escaped = (
            line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        document_xml.append(f"<w:p><w:r><w:t>{escaped}</w:t></w:r></w:p>")
    document_xml.extend(["</w:body>", "</w:document>"])

    with ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", "".join(document_xml))


@pytest.fixture
def app_client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


@pytest.fixture
def complete_resume():
    return COMPLETE_RESUME


@pytest.fixture
def minimal_resume():
    return MINIMAL_RESUME


@pytest.fixture
def matching_resume():
    return MATCHING_RESUME


@pytest.fixture
def mismatch_resume():
    return MISMATCH_RESUME


@pytest.fixture
def job_description():
    return JOB_DESCRIPTION


@pytest.fixture
def pdf_fixture(tmp_path):
    path = tmp_path / "fictional-resume.pdf"
    _write_pdf(path, COMPLETE_RESUME)
    return path


@pytest.fixture
def docx_fixture(tmp_path):
    path = tmp_path / "fictional-resume.docx"
    _write_docx(path, COMPLETE_RESUME)
    return path


@pytest.fixture
def short_pdf_fixture(tmp_path):
    path = tmp_path / "short-resume.pdf"
    _write_pdf(path, "Too short")
    return path
