from pathlib import Path

from app import build_analysis_result


ROOT = Path(__file__).parents[1]


def test_analysis_payload_contains_dashboard_sources(complete_resume, job_description):
    result = build_analysis_result(complete_resume, job_description, "fixture.pdf")

    assert isinstance(result["overall_ats_score"], (int, float))
    assert isinstance(result["matched_skills"], list)
    assert isinstance(result["missing_skills"], list)
    assert isinstance(result["recommendation_details"], list)
    assert isinstance(result["resume_evidence"], dict)
    assert isinstance(result["interview_questions"], list)
    assert result["job_description_present"] is True


def test_result_template_contains_unified_dashboard_sections():
    template = (ROOT / "templates" / "result.html").read_text(encoding="utf-8")

    for marker in ("overviewStrengths", "overviewPriority", "overviewMatch", "recommendations", "interviewQuestions", "rewrites", "matchedSkills", "missingSkills"):
        assert marker in template
    assert "Review improvements" in template
    assert "Open rewriter" in template
    assert "Prepare interview" in template


def test_result_script_supports_empty_states_and_structured_metadata():
    script = (ROOT / "static" / "js" / "result.js").read_text(encoding="utf-8")

    assert "displayOverview" in script
    assert "No evidence-backed strengths yet." in script
    assert "No priority improvements detected." in script
    assert "Add a job description to compare alignment." in script
    assert "recommendation_details" in script
    assert "No recommendations available." in script
    assert "No interview questions available." in script
    assert "No supported rewrite candidates were found" in script
