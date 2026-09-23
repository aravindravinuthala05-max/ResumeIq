import json

from app import build_analysis_result


def test_coach_is_structured_evidence_grounded_and_json_safe(complete_resume, job_description):
    result = build_analysis_result(complete_resume, job_description, "coach.pdf")
    coach = result["interview_coach"]
    assert coach["fact_safe"] is True
    assert coach["roadmap"]
    assert coach["questions"]
    assert all({"question", "category", "difficulty", "priority", "source", "evidence", "reason", "what_to_prepare", "answer_structure", "fact_safe"} <= set(item) for item in coach["questions"])
    assert all(item["fact_safe"] for item in coach["questions"])
    json.dumps(coach)


def test_coach_keeps_jd_gaps_as_unevidenced_preparation(complete_resume):
    result = build_analysis_result(complete_resume, "Python Kubernetes", "gap.pdf")
    gaps = [item for item in result["interview_coach"]["questions"] if item["source"] == "job_description"]
    assert gaps
    assert all(item["status"] == "Not evidenced in resume" for item in gaps)
    assert all("not evidenced" in item["reason"].lower() for item in gaps)
    assert all(item["what_to_learn_first"] and item["how_to_practise"] for item in gaps)
    assert all("not currently represented" in " ".join(item["interview_preparation"]) for item in gaps)
    assert "kubernetes" in result["missing_skills"]


def test_coach_does_not_change_legacy_question_payload(complete_resume, job_description):
    first = build_analysis_result(complete_resume, job_description, "one.pdf")
    second = build_analysis_result(complete_resume, job_description, "two.pdf")
    assert first["interview_questions"] == second["interview_questions"]
    assert first["overall_ats_score"] == second["overall_ats_score"]


def test_template_and_script_expose_coach_explanations():
    from pathlib import Path
    root = Path(__file__).parents[1]
    assert "interviewRoadmap" in (root / "templates" / "result.html").read_text(encoding="utf-8")
    script = (root / "static" / "js" / "result.js").read_text(encoding="utf-8")
    for marker in ("displayInterviewCoach", "Why this question", "What to prepare", "What to learn first", "How to practise", "Answer structure"):
        assert marker in script
