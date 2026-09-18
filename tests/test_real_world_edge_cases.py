import json
from io import BytesIO
from zipfile import ZipFile

import pytest
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas

from app import build_analysis_result, extract_docx_text, extract_resume_text
from resume_rewriter import rewrite_resume
from section_detector import detect_resume_sections

from edge_case_fixtures import EDGE_CASES, SCENARIOS


@pytest.mark.parametrize("case", EDGE_CASES, ids=[item["name"] for item in EDGE_CASES])
def test_real_world_resume_pipeline_contract(case, app_client):
    result = build_analysis_result(case["resume"], case["job_description"], f"{case['name']}.txt")

    assert result["success"] is True
    assert result["resume_text"] == case["resume"]
    assert result["job_description_present"] is bool(case["job_description"])
    assert 0 <= result["overall_ats_score"] <= 100
    assert isinstance(result["score_breakdown"], dict)
    assert isinstance(result["resume_evidence"], dict)
    assert isinstance(result["recommendation_details"], list)
    assert isinstance(result["interview_questions"], list)
    json.dumps(result)

    detected = detect_resume_sections(case["resume"])
    assert case["sections"] <= {name for name, present in detected.items() if present}

    for record_group in result["resume_evidence"].values():
        for record in record_group:
            assert record["value"]
            assert record["source_text"]
            assert record["section"]

    for recommendation in result["recommendation_details"]:
        assert recommendation["fact_safe"] is True
        assert recommendation["priority"] in {"HIGH", "MEDIUM", "LOW"}

    rewrite = rewrite_resume(
        case["resume"],
        case["job_description"],
        {
            "resume_evidence": result["resume_evidence"],
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"],
        },
    )
    assert rewrite["provider"] == "rule_based"
    assert isinstance(rewrite["rewrites"], list)
    assert all(item["fact_safe"] is True for item in rewrite["rewrites"])
    for item in rewrite["rewrites"]:
        assert item["original"] in case["resume"]
        assert item["section"] in {"summary", "experience", "project", "skills", "education"}
        for missing_skill in result["missing_skills"]:
            clean_skill = missing_skill.split(" (", 1)[0].casefold()
            assert clean_skill not in item["rewritten"].casefold()

    for question in result["interview_questions"]:
        assert question["fact_safe"] is True
        if question["source"] == "resume":
            assert all(str(evidence).casefold() in case["resume"].casefold() for evidence in question["evidence"])
        if question["category"] == "JD gap":
            assert question["source"] == "job_description"

    response = app_client.post("/generate_pdf", json=result)
    assert response.status_code == 200
    assert response.content_type == "application/pdf"
    assert response.data.startswith(b"%PDF-")


@pytest.mark.parametrize(
    "resume_text,filename,extractor",
    [
        (SCENARIOS["student_resume"]["resume"], "student.pdf", "pdf"),
        (SCENARIOS["experienced_multiple_employers"]["resume"], "experienced.docx", "docx"),
    ],
)
def test_real_world_pdf_and_docx_extraction(tmp_path, resume_text, filename, extractor):
    path = tmp_path / filename
    if extractor == "pdf":
        document = canvas.Canvas(str(path))
        y = 800
        for line in resume_text.splitlines():
            document.drawString(40, y, line)
            y -= 14
        document.save()
        extracted = extract_resume_text(path, filename)
    else:
        document_xml = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>',
        ]
        for line in resume_text.splitlines():
            escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            document_xml.append(f"<w:p><w:r><w:t>{escaped}</w:t></w:r></w:p>")
        document_xml.append("</w:body></w:document>")
        with ZipFile(path, "w") as archive:
            archive.writestr("word/document.xml", "".join(document_xml))
        extracted = extract_docx_text(path)

    assert extracted.strip()
    assert resume_text.splitlines()[0] in extracted
    assert "Python" in extracted


def test_metrics_and_dates_remain_traceable_through_pipeline():
    case = SCENARIOS["numerical_metrics"]
    result = build_analysis_result(case["resume"], case["job_description"], "metrics.txt")
    evidence = result["resume_evidence"]

    for value in ("45%", "1200 users", "3.5 million", "$25K"):
        assert any(item["value"].casefold() == value.casefold() for item in evidence["metrics"])
    for value in ("2021", "2024"):
        assert any(item["value"] == value for item in evidence["dates"])

    rewrite = rewrite_resume(case["resume"], case["job_description"], {"resume_evidence": evidence})
    for item in rewrite["rewrites"]:
        original_metrics = [value for value in ("45%", "1200 users", "3.5 million", "$25K") if value.casefold() in item["original"].casefold()]
        original_dates = [value for value in ("2021", "2024") if value in item["original"]]
        assert all(value.casefold() in item["rewritten"].casefold() for value in original_metrics)
        assert all(value in item["rewritten"] for value in original_dates)


def test_project_and_employer_facts_do_not_cross_contaminate():
    project_case = SCENARIOS["multiple_projects_technologies"]
    result = build_analysis_result(project_case["resume"], project_case["job_description"], "projects.txt")
    project_records = result["resume_evidence"]["projects"]
    assert any("Vision Tool" in item["value"] for item in project_records)
    assert any("Commerce API" in item["value"] for item in project_records)
    assert any("Mobile Client" in item["value"] for item in project_records)

    rewrite = rewrite_resume(project_case["resume"], project_case["job_description"], result)
    rewrites_by_original = {item["original"]: item["rewritten"] for item in rewrite["rewrites"]}
    assert "Java" not in rewrites_by_original.get("Vision Tool: Python, OpenCV, TensorFlow", "")
    assert "Python" not in rewrites_by_original.get("Commerce API: Java, Spring Boot, MySQL", "")

    employer_case = SCENARIOS["multiple_employers_roles"]
    employer_result = build_analysis_result(employer_case["resume"], employer_case["job_description"], "roles.txt")
    experience_values = {item["value"] for item in employer_result["resume_evidence"]["experience"]}
    assert {"Oak Systems", "Pine Systems", "Birch Group"} <= experience_values
    assert {"Lead Engineer", "Software Engineer", "Analyst"} <= experience_values


def test_jd_only_skills_stay_missing_and_create_safe_questions():
    case = SCENARIOS["many_missing_jd_skills"]
    result = build_analysis_result(case["resume"], case["job_description"], "gaps.txt")
    missing = {skill.split(" (", 1)[0].casefold() for skill in result["missing_skills"]}
    evidence_text = json.dumps(result["resume_evidence"]).casefold()

    assert {"python", "flask", "aws", "docker"} <= missing
    for skill in missing:
        assert skill not in evidence_text
    assert any(item["category"] == "JD gap" for item in result["interview_questions"])
    assert all(item["source"] != "resume" or not any(skill in item["evidence"] for skill in missing) for item in result["interview_questions"])


def test_pdf_report_contains_major_analysis_headings(app_client):
    case = SCENARIOS["student_resume"]
    result = build_analysis_result(case["resume"], case["job_description"], "student.pdf")
    response = app_client.post("/generate_pdf", json=result)

    text = "".join(page.extract_text() or "" for page in PdfReader(BytesIO(response.data)).pages)
    for heading in ("Resume Overview", "ATS / JD Match", "Strengths", "Priority Improvements", "Skills", "Interview Preparation"):
        assert heading in text
