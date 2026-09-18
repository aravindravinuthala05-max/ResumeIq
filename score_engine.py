"""Deterministic, explainable 100-point ATS scoring engine."""

import re


WEIGHTS = {
    "skills": 40,
    "projects": 15,
    "experience": 15,
    "education": 10,
    "sections": 10,
    "formatting": 10,
}


def _clamp(value, maximum):
    return round(max(0, min(float(value), maximum)), 2)


def _projects_score(projects, skills_percent):
    if not projects.get("project_found"):
        return 0.0
    total = projects.get("total_projects", 0)
    volume = 2 if total == 1 else 3.5 if total == 2 else 5 if total >= 3 else 0
    categories = sum(bool(projects.get(key, 0)) for key in ("ai_projects", "web_projects", "mobile_projects", "iot_projects"))
    complexity = min(5, 2 + categories)
    relevance = (skills_percent / 100) * 5
    return _clamp(volume + complexity + relevance, WEIGHTS["projects"])


def _experience_score(resume_text, job_description, experience):
    if not experience.get("experience_found"):
        return 0.0
    internships = min(experience.get("internships", 0), 2)
    companies = min(len(experience.get("companies", [])), 2)
    roles = experience.get("roles", [])
    relevant_roles = sum(role.lower() in job_description.lower() for role in roles)
    years = sorted({int(year) for year in re.findall(r"\b(?:19|20)\d{2}\b", resume_text)})
    estimated_years = min(2, max(0, len(years) - 1))
    return _clamp(4 + internships * 2 + companies * 1.5 + min(3, len(roles)) + min(2, relevant_roles) + estimated_years, WEIGHTS["experience"])


def _education_score(education, job_description):
    if not education.get("education_found"):
        return 0.0
    score = 3
    if education.get("degree") not in (None, "", "Not Found"):
        score += 3
    branch = education.get("branch", "")
    if branch and branch != "Not Found":
        score += 2 if any(word in job_description.lower() for word in branch.lower().split()) else 1
    cgpa = education.get("cgpa", "Not Found")
    try:
        score += 2 if float(cgpa) >= 7.0 else 1
    except (TypeError, ValueError):
        pass
    return _clamp(score, WEIGHTS["education"])


def _sections_score(resume_text):
    text = resume_text.lower()
    section_checks = (
        "@" in text,  # contact
        any(term in text for term in ("summary", "profile", "objective")),
        any(term in text for term in ("skills", "technical skills", "technologies")),
        any(term in text for term in ("education", "b.tech", "bachelor", "university", "college")),
        any(term in text for term in ("project", "projects")),
        any(term in text for term in ("experience", "internship", "employment", "worked at")),
        any(term in text for term in ("certification", "certificate")),
        any(term in text for term in ("languages", "programming languages", "spoken languages")),
    )
    return round(sum(section_checks) * (WEIGHTS["sections"] / len(section_checks)), 2)


def _status_for(score):
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Very Good"
    if score >= 60:
        return "Good"
    if score >= 40:
        return "Needs Improvement"
    return "Poor"


def calculate_weighted_ats_score(
    resume_text,
    job_description,
    skills_match_info,
    projects_info,
    experience_info,
    education_info,
    sections_info,
    formatting_info,
):
    """Calculate the complete ATS result from existing analyzer outputs.

    `sections_info` is accepted to preserve the existing call contract; the
    score itself checks the eight ATS-relevant sections directly from text.
    """
    skills_percent, matched_skills, missing_skills = skills_match_info
    breakdown = {
        "skills_score": _clamp((skills_percent / 100) * WEIGHTS["skills"], WEIGHTS["skills"]),
        "projects_score": _projects_score(projects_info, skills_percent),
        "experience_score": _experience_score(resume_text, job_description, experience_info),
        "education_score": _education_score(education_info, job_description),
        "sections_score": _sections_score(resume_text),
        "formatting_score": _clamp((formatting_info.get("formatting_score", 0) / 100) * WEIGHTS["formatting"], WEIGHTS["formatting"]),
    }
    overall = round(sum(breakdown.values()), 2)
    return {
        "overall_ats_score": overall,
        "score_breakdown": breakdown,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "status": _status_for(overall),
    }
