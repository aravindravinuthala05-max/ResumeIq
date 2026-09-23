"""Controlled Phase 5B cross-module and PDF safety regressions."""

from io import BytesIO

from PyPDF2 import PdfReader

from app import _pdf_value, build_analysis_result, generate_pdf_report
from ats_engine import calculate_ats_score
from resume_rewriter import rewrite_resume
from score_engine import WEIGHTS


RESUME = """Candidate Example
EDUCATION
B.Tech in Artificial Intelligence and Machine Learning, Example University, Graduation year: 2027, CGPA 8.1
SKILLS
Python, SQL, FastAPI
PROJECTS
ResumeIQ: AI Resume Intelligence Platform built using Python and Flask.
EXPERIENCE
Software Engineering Intern at Example Labs for 6 months.
CERTIFICATIONS
AWS Certified Developer
"""

JD = """Required: Python, FastAPI, REST API design, and Kubernetes.
B.Tech degree required. Minimum CGPA 7.0. Graduates of 2027 are eligible.
Experience building reliable backend services is preferred.
"""


def _analysis():
    return build_analysis_result(RESUME, JD, "phase5b-control.pdf")


def test_phase5b_controlled_analysis_keeps_modules_consistent():
    result = _analysis()
    evidence = result["resume_evidence"]

    assert any(item["value"] == "ResumeIQ" and item["section"] == "projects" for item in evidence["projects"])
    assert any(item["value"] == "B.TECH" and item["section"] == "education" for item in evidence["education"])
    assert {item["value"].casefold() for item in evidence["skills"]} >= {"python", "sql", "fastapi"}
    assert any(item["section"] == "certifications" for item in evidence["certifications"])
    assert {"python", "fastapi"}.issubset(set(result["matched_skills"]))
    assert "kubernetes" in result["missing_skills"]

    # JD requirements stay read-only and category-specific.
    representation = result["jd_representation"]
    assert "kubernetes" in representation["skills"]
    assert representation["semantic_requirements"]
    assert {item["requirement_type"] for item in representation["eligibility_requirements"]} >= {
        "DEGREE", "MIN_CGPA", "GRADUATION_YEAR"
    }
    assert "kubernetes" not in {item["value"].casefold() for item in evidence["skills"]}
    assert all(item["source"] == "job_description" for item in representation["eligibility_requirements"])

    eligibility = result["career_eligibility"]
    assert eligibility["supported_count"] >= 3
    assert all(item["evidence_section"] == "education" for item in eligibility["requirements"])

    # Semantic output remains context, never a candidate skill claim.
    assert result["semantic_matches"]["matches"]
    assert "kubernetes" not in {item["value"].casefold() for item in evidence["technologies"]}

    advisor = next(item for item in result["recommendation_details"] if item["source"] == "job_description")
    assert advisor["action_target"] == "skills-section"
    assert advisor["action_label"] == "Review Skills Intelligence"

    rewritten = rewrite_resume(RESUME, JD, result)
    rewritten_text = " ".join(item["rewritten"] for item in rewritten["rewrites"])
    assert "Kubernetes" not in rewritten_text

    questions = result["interview_questions"]
    assert any(item["category"] == "Project" and "ResumeIQ" in item["evidence"] for item in questions)
    assert any(item["category"] == "JD gap" and item["evidence"] == ["kubernetes"] for item in questions)
    assert all(item["fact_safe"] for item in questions)
    assert any("ResumeIQ" in topic for item in result["interview_coach"]["roadmap"] for topic in item["topics"])


def test_phase5b_ats_result_and_weights_are_preserved():
    result = _analysis()
    ats_score, matched, missing = calculate_ats_score(RESUME, JD)

    assert result["matched_skills"] == matched
    assert result["missing_skills"] == missing
    assert ats_score >= 0
    assert set(result["score_breakdown"]) == {f"{name}_score" for name in WEIGHTS}
    assert WEIGHTS == {
        "skills": 40, "projects": 15, "experience": 15,
        "education": 10, "sections": 10, "formatting": 10,
    }


def test_phase5b_pdf_includes_safe_intelligence_summaries():
    payload = _analysis()
    payload["semantic_matches"] = {
        "matches": [{"requirement": "<b>REST API design</b>", "label": "Related Semantic Match", "evidence": "Python APIs"}]
    }
    payload["career_eligibility"] = {
        "supported_count": 1, "conflict_count": 0, "not_evidenced_count": 1,
        "requirements": [{"requirement": "Graduates of 2027", "status": "NOT_EVIDENCED", "reason": "<script>unsafe</script>"}],
    }
    payload["interview_coach"] = {"roadmap": [{"title": "Project Deep Dive", "topics": ["ResumeIQ", "AWS is not evidenced"]}]}

    document = generate_pdf_report(payload)
    text = "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(document.read())).pages)

    assert "Semantic Job Match (semantic relevance only)" in text
    assert "does not create a resume skill" in text
    assert "Career Eligibility" in text
    assert "NOT_EVIDENCED" in text
    assert "enough evidence to determine" in text
    assert "Interview Coach Preparation Roadmap" in text
    assert _pdf_value("<script>unsafe</script>") == "&lt;script&gt;unsafe&lt;/script&gt;"


def test_phase5b_pdf_hides_internal_evidence_metadata_but_keeps_user_facing_evidence():
    payload = _analysis()
    payload["recommendation_details"] = [{
        "title": "Emphasize Python", "description": "Python is supported by your resume.",
        "priority": "LOW", "section": "Skills", "source": "resume_evidence",
        "evidence": ["Python"], "source_text": "SKILLS: Python", "type": "technology",
        "value": "Python", "provenance": {"internal_id": "private"}, "jd_relevance": True,
    }]
    payload["semantic_matches"] = {"matches": [{
        "requirement": "REST API design", "label": "Related Semantic Match",
        "evidence": "Python APIs", "section": "projects", "type": "technology",
        "source": "resume_evidence", "source_text": "internal", "provenance": {"id": "private"},
    }]}

    document = generate_pdf_report(payload)
    text = "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(document.read())).pages)

    assert "Emphasize Python" in text
    assert "Python APIs" in text
    assert "Resume Evidence" in " ".join(text.split())
    for internal in ("resume_evidence", "source_text", "provenance", "internal_id", "Source:", "Type:"):
        assert internal not in text
    assert "{" not in text and "}" not in text
    for heading in (
        "Overall ATS Score:", "Skills Intelligence", "Semantic Job Match (semantic relevance only)",
        "Career Eligibility", "Smart Insights", "Interview Preparation", "Interview Coach Preparation Roadmap",
    ):
        assert heading in text


def test_phase5b_pdf_allows_missing_new_payloads():
    document = generate_pdf_report({"resume_name": "minimal.pdf"})
    assert document.read().startswith(b"%PDF-")
