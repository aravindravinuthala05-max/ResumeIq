import json

from achievement_analyzer import analyze_achievements
from certification_analyzer import analyze_certifications
from education_analyzer import analyze_education
from experience_analyzer import analyze_experience
from language_analyzer import analyze_languages
from project_analyzer import analyze_projects
from resume_evidence import build_resume_evidence
from resume_rewriter import rewrite_resume
from interview_generator import generate_interview_questions


RESUME = """Candidate
SUMMARY
Backend developer focused on reliable APIs.
SKILLS
Python, python, PYTHON, Flask, SQL
EXPERIENCE
Software Engineer at Amazon
2021 - 2023
Implemented Flask APIs and reduced processing time by 30%.
PROJECTS
ResumeIQ: Flask, Python, PostgreSQL
EDUCATION
B.Tech in Computer Science, Fictional University, CGPA 8.5
CERTIFICATIONS
AWS Certified Developer, 2024
ACHIEVEMENTS
Won coding challenge in 2023; improved response time by 30%.
"""


def evidence():
    return build_resume_evidence(
        RESUME,
        education=analyze_education(RESUME),
        experience=analyze_experience(RESUME),
        projects=analyze_projects(RESUME),
        certifications=analyze_certifications(RESUME),
        achievements=analyze_achievements(RESUME),
        languages=analyze_languages(RESUME),
    )


def test_project_name_and_technology_are_traceable():
    result = evidence()
    project = next(item for item in result["projects"] if item["value"] == "ResumeIQ")
    technology = next(item for item in result["technologies"] if item["value"].casefold() == "flask")
    assert project["source_text"].startswith("ResumeIQ:")
    assert technology["section"] in {"skills", "projects"}
    assert "Flask" in technology["source_text"]


def test_experience_preserves_supported_employer_title_and_source():
    result = evidence()
    assert any(item["value"] == "Amazon" and item["type"] == "company" for item in result["experience"])
    assert any(item["value"] == "Software Engineer" and item["type"] == "job_title" for item in result["experience"])
    assert all(item["source_text"] for item in result["experience"])


def test_education_certification_and_achievement_evidence():
    result = evidence()
    assert any(item["value"] == "Fictional University" for item in result["education"])
    assert any("AWS Certified Developer" in item["value"] for item in result["certifications"])
    assert any("Won coding challenge" in item["value"] for item in result["achievements"])


def test_metrics_and_dates_preserve_original_values():
    result = evidence()
    assert any(item["value"] == "30%" and "30%" in item["source_text"] for item in result["metrics"])
    assert any(item["value"] == "2021" for item in result["dates"])
    assert any(item["value"] == "2024" for item in result["dates"])
    assert not any(item["value"] == "92%" for item in result["metrics"])


def test_duplicate_skills_are_case_insensitively_normalized():
    result = evidence()
    python_values = [item["value"].casefold() for item in result["skills"] if item["value"].casefold() == "python"]
    assert python_values == ["python"]


def test_jd_only_keywords_are_not_evidence():
    result = build_resume_evidence("SKILLS\nPython\nPROJECTS\nA Python tool")
    assert not any(item["value"].casefold() == "aws" for item in result["technologies"])
    assert not any(item["value"].casefold() == "aws" for item in result["skills"])


def test_unsupported_facts_are_not_generated_by_evidence():
    result = build_resume_evidence("PROJECTS\nA Python tool")
    serialized = json.dumps(result).lower()
    assert "aws" not in serialized
    assert "leadership" not in serialized


def test_rewriter_and_interview_remain_compatible_with_shared_evidence():
    result = evidence()
    rewrite = rewrite_resume(RESUME, "Python Flask", {"resume_evidence": result, "matched_skills": ["python", "flask"], "missing_skills": []})
    questions = generate_interview_questions({}, {}, {}, ["python", "flask"], [], "Python Flask", resume_text=RESUME, resume_evidence=result)
    assert rewrite["provider"] == "rule_based"
    assert isinstance(rewrite["rewrites"], list)
    assert any(item["source"] == "resume" and "ResumeIQ" in item["evidence"] for item in questions)
