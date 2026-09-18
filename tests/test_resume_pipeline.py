import json
from io import BytesIO

import pytest

from achievement_analyzer import analyze_achievements
from app import build_analysis_result, extract_docx_text, extract_resume_text
from ats_engine import calculate_ats_score
from certification_analyzer import analyze_certifications
from contact_analyzer import analyze_contact
from education_analyzer import analyze_education
from experience_analyzer import analyze_experience
from formatting_analyzer import analyze_formatting
from language_analyzer import analyze_languages
from project_analyzer import analyze_projects
from resume_rewriter import RewriteProvider, rewrite_resume
from score_engine import calculate_weighted_ats_score
from section_detector import detect_resume_sections


EXPECTED_RESULT_FIELDS = {
    "success",
    "resume_name",
    "analysis_timestamp",
    "overall_ats_score",
    "score_breakdown",
    "matched_skills",
    "missing_skills",
    "contact",
    "education",
    "experience",
    "projects",
    "certifications",
    "languages",
    "achievements",
    "formatting",
    "suggestions",
    "interview_questions",
    "status",
}
EXPECTED_BREAKDOWN_FIELDS = {
    "skills_score",
    "projects_score",
    "experience_score",
    "education_score",
    "sections_score",
    "formatting_score",
}


def test_pdf_extraction_returns_fixture_text(pdf_fixture):
    extracted = extract_resume_text(pdf_fixture, pdf_fixture.name)

    assert extracted.strip()
    assert "Fictional Candidate" in extracted
    assert "fictional.candidate@example.com" in extracted


def test_docx_extraction_returns_fixture_text(docx_fixture):
    extracted = extract_docx_text(docx_fixture)

    assert extracted.strip()
    assert "Fictional Candidate" in extracted
    assert "AWS Certified Developer" in extracted


def test_all_analyzers_process_complete_fixture(complete_resume):
    contact = analyze_contact(complete_resume)
    education = analyze_education(complete_resume)
    experience = analyze_experience(complete_resume)
    projects = analyze_projects(complete_resume)
    certifications = analyze_certifications(complete_resume)
    achievements = analyze_achievements(complete_resume)
    languages = analyze_languages(complete_resume)
    formatting = analyze_formatting(complete_resume)
    sections = detect_resume_sections(complete_resume)

    assert contact["email"] == "fictional.candidate@example.com"
    assert education["education_found"] is True
    assert experience["experience_found"] is True
    assert projects["project_found"] is True
    assert certifications["has_certifications"] is True
    assert achievements["has_metrics"] is True
    assert languages["total_languages"] > 0
    assert 0 <= formatting["formatting_score"] <= 100
    assert all(isinstance(value, bool) for value in sections.values())
    assert sections["Education"] is True
    assert sections["Experience"] is True
    assert sections["Projects"] is True
    assert sections["Skills"] is True
    assert sections["Certifications"] is True


def test_ats_matching_resume_matches_required_skills(matching_resume, job_description):
    score, matched, missing = calculate_ats_score(matching_resume, job_description)

    assert score > 0
    assert {"python", "flask", "sql", "postgresql", "aws", "docker", "git"}.issubset(set(matched))
    assert isinstance(missing, list)
    assert 0 <= score <= 100


def test_ats_mismatch_resume_reports_missing_skills(mismatch_resume, job_description):
    score, matched, missing = calculate_ats_score(mismatch_resume, job_description)

    assert score == 0
    assert matched == []
    assert missing


def test_weighted_score_contract(complete_resume, job_description):
    skills_match = calculate_ats_score(complete_resume, job_description)
    result = build_analysis_result(complete_resume, job_description, "fictional.pdf")

    assert isinstance(result["overall_ats_score"], (int, float))
    assert 0 <= result["overall_ats_score"] <= 100
    assert set(result["score_breakdown"]) == EXPECTED_BREAKDOWN_FIELDS
    assert all(0 <= value <= limit for value, limit in zip(
        result["score_breakdown"].values(), [40, 15, 15, 10, 10, 10]
    ))
    assert skills_match[0] >= 0


def test_build_analysis_result_contains_existing_fields(complete_resume, job_description):
    result = build_analysis_result(complete_resume, job_description, "fictional-resume.pdf")

    assert result["success"] is True
    assert EXPECTED_RESULT_FIELDS.issubset(result)
    assert result["resume_name"] == "fictional-resume.pdf"
    assert result["resume_text"] == complete_resume
    assert result["status"]
    assert isinstance(result["suggestions"], list)
    assert isinstance(result["interview_questions"], list)
    json.dumps(result)


@pytest.mark.parametrize("path", ["/", "/result", "/features", "/how-it-works", "/about", "/contact"])
def test_get_pages(app_client, path):
    response = app_client.get(path)

    assert response.status_code == 200
    assert response.content_type.startswith("text/html")


def test_health_route(app_client):
    response = app_client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy", "service": "ResumeIQ"}


def test_upload_rejects_missing_resume(app_client, job_description):
    response = app_client.post("/upload", data={"job_description": job_description})

    assert response.status_code == 400
    assert response.get_json()["error"] == "No resume file uploaded"


def test_upload_rejects_empty_filename(app_client, job_description):
    response = app_client.post(
        "/upload",
        data={"resume": (BytesIO(b""), ""), "job_description": job_description},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "No file selected"


def test_upload_rejects_missing_job_description(app_client, pdf_fixture):
    with pdf_fixture.open("rb") as resume:
        response = app_client.post("/upload", data={"resume": (resume, "resume.pdf")})

    assert response.status_code == 400
    assert response.get_json()["error"] == "No job description provided"


def test_upload_rejects_unsupported_extension(app_client, job_description):
    response = app_client.post(
        "/upload",
        data={"resume": (BytesIO(b"not a resume"), "resume.txt"), "job_description": job_description},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Please upload a PDF or DOCX resume"


def test_upload_rejects_oversized_request_with_json_error(app_client, job_description):
    response = app_client.post(
        "/upload",
        data={"resume": (BytesIO(b"x" * (16 * 1024 * 1024 + 1)), "large.pdf"), "job_description": job_description},
    )

    assert response.status_code == 413
    assert response.content_type.startswith("application/json")
    assert "too large" in response.get_json()["error"].lower()


def test_upload_rejects_insufficient_extracted_text(app_client, short_pdf_fixture, job_description):
    with short_pdf_fixture.open("rb") as resume:
        response = app_client.post(
            "/upload",
            data={"resume": (resume, "short.pdf"), "job_description": job_description},
        )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Could not extract enough text from the uploaded resume"


@pytest.mark.parametrize("extension,fixture_name", [("pdf", "pdf_fixture"), ("docx", "docx_fixture")])
def test_upload_accepts_supported_resume_formats(app_client, job_description, request, extension, fixture_name):
    fixture = request.getfixturevalue(fixture_name)
    with fixture.open("rb") as resume:
        response = app_client.post(
            "/upload",
            data={"resume": (resume, f"fictional-resume.{extension}"), "job_description": job_description},
        )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["resume_name"].endswith(f".{extension}")


def test_generate_pdf_returns_valid_pdf(app_client, complete_resume, job_description):
    analysis = build_analysis_result(complete_resume, job_description, "fictional.pdf")
    response = app_client.post("/generate_pdf", json=analysis)

    assert response.status_code == 200
    assert response.content_type == "application/pdf"
    assert response.data.startswith(b"%PDF-")
    assert len(response.data) > 100


def test_generate_pdf_rejects_missing_payload(app_client):
    response = app_client.post("/generate_pdf", json={})

    assert response.status_code == 400
    assert response.get_json()["error"] == "No analysis data provided"


def test_pipeline_handles_minimal_and_empty_optional_data(minimal_resume):
    result = build_analysis_result(minimal_resume, "Rust quantum computing", "minimal.pdf")

    assert result["success"] is True
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []
    assert result["education"]["education_found"] is False
    assert result["experience"]["experience_found"] is False
    assert result["projects"]["project_found"] is False
    assert isinstance(result["suggestions"], list)
    assert isinstance(result["interview_questions"], list)


def test_generate_pdf_handles_edge_payload(app_client):
    payload = {
        "resume_name": "unicode-resume-\u2605.pdf",
        "analysis_timestamp": "2026-09-12T00:00:00",
        "overall_ats_score": 0,
        "score_breakdown": {},
        "matched_skills": [],
        "missing_skills": ["A" * 300],
        "contact": {"email": "edge@example.com", "location": "Tokyo & Remote"},
        "education": {},
        "experience": {},
        "projects": {},
        "certifications": {},
        "achievements": {},
        "languages": {},
        "suggestions": [],
        "interview_questions": [],
        "formatting": {},
        "status": "Poor",
    }
    response = app_client.post("/generate_pdf", json=payload)

    assert response.status_code == 200
    assert response.data.startswith(b"%PDF-")


def test_generate_pdf_escapes_hostile_html_like_values(app_client):
    payload = {
        "resume_name": "<script>alert(1)</script>.pdf",
        "analysis_timestamp": "2026-09-16T00:00:00",
        "overall_ats_score": 0,
        "score_breakdown": {},
        "matched_skills": ["<b>Python</b>"],
        "missing_skills": [],
        "contact": {"summary": "<script>alert(1)</script>"},
        "education": {},
        "experience": {},
        "projects": {},
        "certifications": {},
        "achievements": {},
        "languages": {},
        "suggestions": [],
        "recommendation_details": [],
        "interview_questions": [],
        "formatting": {},
        "status": "Poor",
    }

    response = app_client.post("/generate_pdf", json=payload)

    assert response.status_code == 200
    assert response.content_type == "application/pdf"
    assert response.data.startswith(b"%PDF-")


def test_rewriter_returns_structured_fact_safe_rewrites():
    resume = """SUMMARY
I worked on Python APIs.
EXPERIENCE
Responsible for Flask services.
SKILLS
Python, Flask, SQL
"""

    result = rewrite_resume(resume, "Python Flask SQL AWS")

    assert result["provider"] == "rule_based"
    assert result["mode"] == "deterministic_fallback"
    assert result["rewrites"]
    assert all(item["fact_safe"] is True for item in result["rewrites"])
    assert all({"section", "original", "rewritten", "reason", "keywords", "fact_safe"}.issubset(item) for item in result["rewrites"])
    assert any("flask" in item["keywords"] for item in result["rewrites"])
    assert "aws" in result["missing_keywords"]


def test_rewriter_does_not_invent_facts():
    resume = """EXPERIENCE
Responsible for internal tools.
"""

    result = rewrite_resume(resume, "Python AWS Google")
    rewritten = " ".join(item["rewritten"] for item in result["rewrites"])

    assert "Google" not in rewritten
    assert "AWS" not in rewritten
    assert "Python" not in rewritten


def test_rewriter_preserves_experience_facts_and_reports_source():
    result = rewrite_resume("EXPERIENCE\nI worked on Python APIs for 2 years.", "Python")

    item = result["rewrites"][0]
    assert "Python" in item["rewritten"]
    assert "2 years" in item["rewritten"]
    assert {"keyword": "python", "status": "supported", "source": "experience"} in item["keyword_evidence"]
    assert "action" in item["reason"].lower() or "wording" in item["reason"].lower()


def test_rewriter_preserves_project_technologies():
    result = rewrite_resume("PROJECTS\nMade a Python project using Flask.", "Python Flask")

    item = result["rewrites"][0]
    assert "Python" in item["rewritten"]
    assert "Flask" in item["rewritten"]
    assert item["fact_safe"] is True


def test_rewriter_items_keep_source_section_and_exact_original_text():
    resume = """SUMMARY
I worked on reliable APIs.
SKILLS
Python, Flask, SQL, Git
"""

    result = rewrite_resume(resume, "Python Flask SQL Git")

    assert [(item["section"], item["original"]) for item in result["rewrites"]] == [
        ("summary", "I worked on reliable APIs."),
        ("skills", "Python, Flask, SQL, Git"),
    ]
    assert result["rewrites"][0]["rewritten"] == "I contributed to reliable APIs."
    assert result["rewrites"][1]["rewritten"] == "Technical skills: Python, Flask, SQL, Git"


def test_rewriter_omits_unchanged_content_instead_of_faking_improvement():
    result = rewrite_resume("SUMMARY\nExperienced Python developer.", "Python")

    assert result["rewrites"] == []
    assert "No supported rewrite candidates" in result["message"]


def test_rewriter_keeps_multiple_sections_independent():
    result = rewrite_resume(
        "SUMMARY\nI worked on APIs.\nPROJECTS\nMade a Python project.",
        "Python",
    )

    assert [item["section"] for item in result["rewrites"]] == ["summary", "project"]
    assert result["rewrites"][0]["original"] == "I worked on APIs."
    assert result["rewrites"][1]["original"] == "Made a Python project."
    assert "Python" not in result["rewrites"][0]["original"]


def test_summary_rewrite_does_not_invent_experience():
    result = rewrite_resume("SUMMARY\nPython developer interested in APIs.", "Python AWS")

    rewritten = " ".join(item["rewritten"] for item in result["rewrites"])
    assert "AWS" not in rewritten
    assert "experience" not in rewritten.lower()


def test_education_rewrite_does_not_invent_degree():
    result = rewrite_resume("EDUCATION\nState University, Computer Science", "Python")

    assert result["rewrites"][0]["rewritten"] == "State University | Computer Science"
    assert "BTECH" not in result["rewrites"][0]["rewritten"]


def test_supported_keyword_is_explicitly_supported():
    result = rewrite_resume(
        "PROJECTS\nI used Python to build a tool.",
        "Python AWS",
        {"matched_skills": ["python"], "missing_skills": ["aws"]},
    )

    assert result["keyword_evidence"]
    assert {"keyword": "python", "status": "supported", "source": "project"} in result["keyword_evidence"]
    assert {"keyword": "aws", "status": "unsupported", "source": "none"} in result["keyword_evidence"]
    assert "aws" in result["missing_keywords"]


def test_keyword_supported_elsewhere_is_not_inserted_into_other_rewrite():
    result = rewrite_resume(
        "PROJECTS\nI worked on a tool.\nSKILLS\nPython, Flask",
        "Python Flask",
        {"matched_skills": ["python", "flask"], "missing_skills": []},
    )

    project_item = result["rewrites"][0]
    assert project_item["section"] == "project"
    assert project_item["keywords"] == []
    assert "Python" not in project_item["rewritten"]


def test_custom_provider_unsupported_metric_falls_back_to_original():
    class UnsafeProvider(RewriteProvider):
        name = "unsafe_test_provider"

        def rewrite(self, resume_text, job_description="", analysis=None):
            return {"provider": self.name, "rewrites": [{
                "section": "experience",
                "original": "I worked on internal tools.",
                "rewritten": "Improved internal tools by 50%.",
                "reason": "Added impact.",
                "keywords": [],
            }]}

    result = rewrite_resume("EXPERIENCE\nI worked on internal tools.", provider=UnsafeProvider())

    item = result["rewrites"][0]
    assert item["rewritten"] == item["original"]
    assert item["fact_safe"] is False
    assert "50" in item["safety_issues"]
    assert result["fact_safe"] is False


def test_custom_provider_unsupported_technology_falls_back_to_original():
    class UnsafeProvider(RewriteProvider):
        name = "unsafe_test_provider"

        def rewrite(self, resume_text, job_description="", analysis=None):
            return {"provider": self.name, "rewrites": [{
                "section": "project",
                "original": "Created a Python project.",
                "rewritten": "Created a Python and AWS project.",
                "reason": "Clarified technology.",
                "keywords": [],
            }]}

    result = rewrite_resume("PROJECTS\nCreated a Python project.", provider=UnsafeProvider())

    item = result["rewrites"][0]
    assert item["rewritten"] == item["original"]
    assert item["fact_safe"] is False
    assert "aws" in item["safety_issues"]


def test_rewriter_response_remains_backward_compatible():
    result = rewrite_resume("SKILLS\nPython, Flask", "Python Flask")

    assert {"provider", "mode", "rewrites", "missing_keywords", "message"}.issubset(result)
    assert isinstance(result["rewrites"], list)
    assert isinstance(result["keyword_evidence"], list)


def test_rewriter_handles_missing_sections_and_unsupported_candidates():
    result = rewrite_resume("CONTACT\nfictional@example.com\n", "Python")

    assert result["rewrites"] == []
    assert "No supported rewrite candidates" in result["message"]


def test_rewrite_endpoint_accepts_valid_request(app_client):
    response = app_client.post(
        "/rewrite",
        json={
            "resume_text": "PROJECTS\nI used Python and Flask to build an internal tool.",
            "job_description": "Python Flask AWS",
            "analysis": {"matched_skills": ["python", "flask"], "missing_skills": ["aws"]},
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["provider"] == "rule_based"
    assert payload["rewrites"][0]["section"] == "project"
    json.dumps(payload)


@pytest.mark.parametrize(
    "payload, expected_error",
    [
        (None, "A JSON object is required"),
        ({}, "resume_text is required"),
        ({"resume_text": "   "}, "resume_text is required"),
        ({"resume_text": 123}, "resume_text is required"),
        ({"resume_text": "SUMMARY\nI worked on tools.", "job_description": 123}, "job_description must be a string"),
        ({"resume_text": "SUMMARY\nI worked on tools.", "analysis": []}, "analysis must be an object"),
    ],
)
def test_rewrite_endpoint_validates_input(app_client, payload, expected_error):
    response = app_client.post("/rewrite", json=payload)

    assert response.status_code == 400
    assert response.get_json()["error"] == expected_error


def test_rewrite_endpoint_allows_empty_job_description(app_client):
    response = app_client.post("/rewrite", json={"resume_text": "SUMMARY\nI worked on tools."})

    assert response.status_code == 200
    assert response.get_json()["provider"] == "rule_based"
