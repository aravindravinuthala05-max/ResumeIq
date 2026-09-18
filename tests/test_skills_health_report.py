from io import BytesIO
from pathlib import Path

from PyPDF2 import PdfReader

from app import build_analysis_result


ROOT = Path(__file__).parents[1]


def test_skills_payload_distinguishes_resume_matched_missing_and_evidence(complete_resume, job_description):
    result = build_analysis_result(complete_resume, job_description, "skills.pdf")
    resume_skills = {item["value"].casefold() for item in result["resume_evidence"]["skills"]}
    evidence_skills = {item["value"].casefold() for item in result["resume_evidence"]["technologies"]}
    matched = {skill.split(" (", 1)[0].casefold() for skill in result["matched_skills"]}
    missing = {skill.split(" (", 1)[0].casefold() for skill in result["missing_skills"]}

    assert "python" in resume_skills
    assert "python" in matched
    assert "python" in evidence_skills
    assert missing.isdisjoint(resume_skills)
    assert missing.isdisjoint(evidence_skills)


def test_result_template_contains_skills_health_and_safe_empty_markers():
    template = (ROOT / "templates" / "result.html").read_text(encoding="utf-8")
    script = (ROOT / "static" / "js" / "result.js").read_text(encoding="utf-8")

    for marker in ("resumeSkills", "matchedSkills", "missingSkills", "evidenceSkills", "healthAtsScore", "healthJdMatch", "healthPriorityCount", "healthRewriteCount", "healthInterviewCount"):
        assert marker in template
        assert marker in script
    assert "Not currently supported by your resume" in template
    assert "No resume skills identified." in script
    assert "No evidence-backed skills available." in script


def test_no_jd_health_and_skills_use_existing_empty_states(minimal_resume):
    result = build_analysis_result(minimal_resume, "", "minimal.txt")

    assert result["job_description_present"] is False
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []
    assert result["resume_evidence"]["skills"]
    assert isinstance(result["recommendation_details"], list)


def test_health_counts_use_existing_values_and_missing_fields_stay_unknown():
    script = (ROOT / "static" / "js" / "result.js").read_text(encoding="utf-8")

    assert "Number.isFinite(score) ? `${score.toFixed(1)}%` : 'Unknown'" in script
    assert "No job description" in script
    assert "asArray(data.interview_questions).length" in script
    assert "item.priority === 'HIGH'" in script
    assert "Available when opened" in (ROOT / "templates" / "result.html").read_text(encoding="utf-8")


def test_pdf_contains_phase_headings_and_handles_empty_sections(app_client, minimal_resume):
    result = build_analysis_result(minimal_resume, "", "minimal.pdf")
    response = app_client.post("/generate_pdf", json=result)

    assert response.status_code == 200
    assert response.content_type == "application/pdf"
    assert response.data.startswith(b"%PDF-")
    text = "".join(page.extract_text() or "" for page in PdfReader(BytesIO(response.data)).pages)
    for heading in ("Resume Overview", "ATS / JD Match", "Strengths", "Priority Improvements", "Skills", "Interview Preparation"):
        assert heading in text
    assert "No information detected in this resume." in text
    assert '"overall_ats_score"' not in text
