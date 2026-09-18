"""Skill matching utilities used by the ResumeIQ ATS scoring engine."""

import re

from skills import AI_ML, CLOUD, DATABASES, DEVOPS, FRAMEWORKS, PROGRAMMING_LANGUAGES


ALL_SKILLS = tuple(dict.fromkeys(
    PROGRAMMING_LANGUAGES + FRAMEWORKS + DATABASES + CLOUD + AI_ML + DEVOPS
))

# Alternate spellings map to one display/canonical skill.  They make matching
# resilient without treating unrelated terms as a match.
SKILL_ALIASES = {
    "c++": ("c++", "cpp"),
    "javascript": ("javascript", "java script", "js"),
    "typescript": ("typescript", "type script", "ts"),
    "spring boot": ("spring boot", "springboot"),
    "postgresql": ("postgresql", "postgres"),
    "aws": ("aws", "amazon web services"),
    "gcp": ("gcp", "google cloud", "google cloud platform"),
    "machine learning": ("machine learning", "ml"),
    "scikit-learn": ("scikit-learn", "scikit learn", "sklearn"),
    "hugging face": ("hugging face", "huggingface"),
}

# A related technology earns partial credit only when it belongs to the same
# technical family as a job requirement.
RELATED_SKILL_GROUPS = (
    {"javascript", "typescript"},
    {"flask", "django", "fastapi"},
    {"mysql", "postgresql", "sql"},
    {"aws", "azure", "gcp"},
    {"machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn"},
    {"docker", "kubernetes", "jenkins"},
)


def _contains_phrase(text, phrase):
    """Match a skill as a term, avoiding false matches such as `c` in `cert`."""
    pattern = r"(?<!\w)" + re.escape(phrase.lower()) + r"(?!\w)"
    return bool(re.search(pattern, text.lower()))


def _skill_present(text, skill):
    aliases = SKILL_ALIASES.get(skill, (skill,))
    return any(_contains_phrase(text, alias) for alias in aliases)


def _related_resume_skill(required_skill, resume_text):
    for group in RELATED_SKILL_GROUPS:
        if required_skill in group:
            return any(skill != required_skill and _skill_present(resume_text, skill) for skill in group)
    return False


def calculate_ats_score(resume_text, job_description):
    """Return a 0-100 skills match and lists of exact/partial/missing skills.

    Exact skill matches contribute 100% and related technologies contribute
    50%.  The returned `matched_skills` list includes only skills actually
    present in the resume, while `missing_skills` remains actionable.
    """
    required_skills = [skill for skill in ALL_SKILLS if _skill_present(job_description, skill)]
    matched_skills = []
    missing_skills = []
    earned_credit = 0.0

    for skill in required_skills:
        if _skill_present(resume_text, skill):
            matched_skills.append(skill)
            earned_credit += 1.0
        elif _related_resume_skill(skill, resume_text):
            # Keep a related technology visible to the user rather than
            # labelling the requirement as fully matched.
            matched_skills.append(f"{skill} (related experience)")
            missing_skills.append(skill)
            earned_credit += 0.5
        else:
            missing_skills.append(skill)

    score = round((earned_credit / len(required_skills)) * 100, 2) if required_skills else 0.0
    return score, matched_skills, missing_skills
