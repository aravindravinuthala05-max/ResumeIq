from achievement_analyzer import analyze_achievements
from education_analyzer import analyze_education
from experience_analyzer import analyze_experience
from project_analyzer import analyze_projects
from resume_advisor import generate_advice
from resume_evidence import build_resume_evidence


RESUME = """Candidate
SUMMARY
Backend developer.
SKILLS
Python, Flask
EXPERIENCE
Software Engineer at Example Systems
Built internal APIs.
PROJECTS
ResumeIQ: Flask, Python API
EDUCATION
B.Tech in Computer Science, Fictional University
ACHIEVEMENTS
Improved response time by 30%.
"""


def make_evidence(text=RESUME):
    return build_resume_evidence(
        text,
        education=analyze_education(text),
        experience=analyze_experience(text),
        projects=analyze_projects(text),
        achievements=analyze_achievements(text),
    )


def advice(**overrides):
    values = {
        "missing_skills": [],
        "matched_skills": ["python", "flask"],
        "formatting_issues": [],
        "achievements_info": {"quantified_achievements": 1},
        "sections_present": {"Summary": True},
        "score_breakdown": {},
        "resume_evidence": make_evidence(),
        "job_description": "Python Flask backend role",
    }
    values.update(overrides)
    return generate_advice(**values)


def test_evidence_backed_and_jd_match_recommendations():
    result = advice()
    item = next(item for item in result["recommendations"] if item["title"].casefold().startswith("emphasize python"))
    assert item["source"] == "resume_evidence"
    assert item["jd_relevance"] is True
    assert item["fact_safe"] is True


def test_jd_gap_does_not_recommend_unsupported_skill_as_existing():
    result = advice(missing_skills=["aws"], matched_skills=[])
    item = next(item for item in result["recommendations"] if item["section"] == "Skills")
    assert item["priority"] == "HIGH"
    assert item["source"] == "job_description"
    assert "not supported" in item["description"]
    assert "genuinely" in item["description"]


def test_project_and_experience_quality_recommendations_are_evidence_backed():
    text = "EXPERIENCE\nSoftware Engineer at Example Systems\nPROJECTS\nResumeIQ"
    result = advice(
        resume_evidence=make_evidence(text),
        achievements_info={},
        sections_present={},
        matched_skills=[],
        job_description="",
    )
    assert any(item["section"] == "Projects" for item in result["recommendations"])
    assert any(item["section"] == "Experience" for item in result["recommendations"])


def test_strengths_are_only_generated_for_supported_matches():
    result = advice(matched_skills=["aws"])
    assert not any(item["title"].startswith("Emphasize aws") for item in result["recommendations"])
    result = advice(matched_skills=["python"])
    assert any(item["title"].startswith("Emphasize python") for item in result["recommendations"])


def test_priority_order_and_deduplication():
    result = advice(missing_skills=["aws", "aws"], formatting_issues=["Needs bullets", "Needs bullets"])
    priorities = [item["priority"] for item in result["recommendations"]]
    assert priorities == sorted(priorities, key={"HIGH": 0, "MEDIUM": 1, "LOW": 2}.get)
    titles = [(item["title"], item["section"]) for item in result["recommendations"]]
    assert len(titles) == len(set(titles))


def test_factual_safety_and_empty_or_malformed_inputs():
    result = generate_advice(missing_skills="aws", matched_skills=None, resume_evidence="bad", job_description=None)
    assert result["recommendations"]
    assert all(item["fact_safe"] is True for item in result["recommendations"])
    empty = generate_advice()
    assert isinstance(empty["recommendations"], list)
    assert isinstance(empty["suggestions"], list)


def test_legacy_suggestions_remain_available():
    result = advice()
    assert isinstance(result["suggestions"], list)
    assert result["suggestions"]
