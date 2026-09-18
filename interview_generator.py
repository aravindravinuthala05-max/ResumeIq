"""Deterministic, resume-evidence-based interview question generation."""

import re


KNOWN_TECHNOLOGIES = (
    "python", "java", "javascript", "typescript", "react", "flask", "django",
    "sql", "postgresql", "mysql", "mongodb", "aws", "azure", "gcp", "docker",
    "kubernetes", "git", "tensorflow", "pytorch", "machine learning", "rest api",
    "html", "css", "node.js", "node", "opencv", "android", "flutter", "kotlin",
)

SKILL_QUESTIONS = {
    "python": "What role does Python play in the work described on your resume?",
    "java": "Which Java concepts are relevant to the work described on your resume?",
    "javascript": "How did JavaScript support the work described on your resume?",
    "typescript": "Where did TypeScript fit into the work described on your resume?",
    "react": "How did React fit into the project or experience listed on your resume?",
    "flask": "How did Flask fit into the application work listed on your resume?",
    "django": "How did Django fit into the work listed on your resume?",
    "sql": "How did SQL support the data work described on your resume?",
    "postgresql": "Why was PostgreSQL relevant to the work described on your resume?",
    "aws": "What role did AWS play in the work described on your resume?",
    "docker": "How did Docker support the work described on your resume?",
    "git": "How did Git support the projects or experience listed on your resume?",
    "machine learning": "Where does machine learning appear in the work described on your resume?",
    "tensorflow": "How was TensorFlow used in the work described on your resume?",
    "rest api": "How did REST API design relate to the work described on your resume?",
}

SECTION_NAMES = {
    "summary": {"summary", "professional summary", "profile"},
    "skills": {"skills", "technical skills", "key skills"},
    "projects": {"projects", "personal projects", "academic projects"},
    "experience": {"experience", "work experience", "employment"},
    "education": {"education", "academic background"},
    "certifications": {"certifications", "certificates"},
    "achievements": {"achievements", "awards"},
}


def _lines(text):
    return [line.strip() for line in (text or "").splitlines() if line.strip()]


def _section_lines(text, section):
    names = SECTION_NAMES[section]
    lines = _lines(text)
    start = next((index for index, line in enumerate(lines) if line.lower().rstrip(":") in names), None)
    if start is None:
        return []
    result = []
    for line in lines[start + 1:]:
        normalized = line.lower().rstrip(":")
        if any(normalized in values for values in SECTION_NAMES.values()):
            break
        result.append(line)
    return result


def _contains(text, value):
    return bool(re.search(r"(?<![a-z0-9])" + re.escape(value.lower()) + r"(?![a-z0-9])", text.lower()))


def _resume_technologies(resume_text, matched_skills, resume_evidence=None):
    values = []
    for item in (resume_evidence or {}).get("technologies", []):
        if item.get("section") in {"summary", "skills", "projects", "experience"}:
            values.append(item.get("value", ""))
    evidence_lines = []
    for section in ("summary", "skills", "projects", "experience"):
        evidence_lines.extend(_section_lines(resume_text, section))
    evidence_text = "\n".join(evidence_lines)
    for skill in list(matched_skills or []) + list(KNOWN_TECHNOLOGIES):
        if _contains(evidence_text, skill) and skill.lower() not in {item.lower() for item in values}:
            values.append(skill)
    return values


def _add_question(questions, question, category, source, evidence=None, jd_match=False, priority=50):
    if not question or any(item["question"] == question for item in questions):
        return
    questions.append({
        "question": question,
        "category": category,
        "source": source,
        "evidence": list(evidence or []),
        "jd_match": bool(jd_match),
        "priority": priority,
        "fact_safe": True,
    })


def _project_evidence(resume_text):
    evidence = []
    for line in _section_lines(resume_text, "projects"):
        if len(line) < 3:
            continue
        name, _, details = line.partition(":")
        values = [name.strip()]
        values.extend(technology for technology in KNOWN_TECHNOLOGIES if _contains(details or line, technology))
        evidence.append((name.strip(), details.strip() or line, list(dict.fromkeys(values))))
    return evidence


def _experience_evidence(resume_text, experience_info):
    lines = _section_lines(resume_text, "experience")
    if lines:
        role_lines = [line for line in lines if re.search(r"\bat\b", line, re.IGNORECASE)]
        return list(dict.fromkeys(role_lines or lines))
    named = list(experience_info.get("companies", [])) + list(experience_info.get("roles", []))
    return list(dict.fromkeys(named + lines))


def generate_interview_questions(
    projects_info,
    experience_info,
    education_info,
    matched_skills,
    missing_skills,
    job_description,
    resume_text="",
    certifications_info=None,
    achievements_info=None,
    resume_evidence=None,
):
    """Return up to 15 deterministic questions grounded in resume and JD evidence.

    The first six parameters are retained for compatibility with existing callers.
    Resume text and optional analyzer outputs provide richer evidence without any
    external model or provider.
    """
    resume_text = resume_text or ""
    certifications_info = certifications_info or {}
    achievements_info = achievements_info or {}
    questions = []
    resume_lower = resume_text.lower()
    matched_lower = {skill.lower() for skill in (matched_skills or [])}

    for name, details, evidence in _project_evidence(resume_text):
        _add_question(questions, f"Explain the {name} project mentioned on your resume. What problem did it address?", "Project", "resume", evidence, any(item.lower() in matched_lower for item in evidence), 100)
        if details != name:
            _add_question(questions, f"What implementation decisions did you make in the {name} project based on its described technologies or approach?", "Project deep-dive", "resume", evidence, any(item.lower() in matched_lower for item in evidence), 92)

    for item in _experience_evidence(resume_text, experience_info or {})[:3]:
        _add_question(questions, f"What responsibilities or outcomes are represented by {item} on your resume?", "Experience", "resume", [item], False, 88)

    for skill in _resume_technologies(resume_text, matched_skills, resume_evidence):
        key = skill.lower()
        if key in SKILL_QUESTIONS:
            _add_question(questions, SKILL_QUESTIONS[key], "Technical", "resume", [skill], key in matched_lower, 84 if key in matched_lower else 76)

    education_evidence = [
        value for key in ("degree", "branch", "college")
        if (value := (education_info or {}).get(key)) and value != "Not Found" and _contains(resume_text, value)
    ]
    if education_evidence:
        _add_question(questions, f"How does your {education_evidence[0]} background relate to this role?", "Education", "resume", education_evidence, False, 70)

    certification_values = []
    for key in ("aws_certifications", "gcp_certifications", "azure_certifications", "other_certifications"):
        certification_values.extend(certifications_info.get(key, []))
    certification_values = [value for value in certification_values if _contains(resume_text, value)]
    if certification_values:
        _add_question(questions, f"What did you learn through {certification_values[0]} that is relevant to this role?", "Certification", "resume", [certification_values[0]], certification_values[0].lower() in matched_lower, 68)

    achievement_lines = _section_lines(resume_text, "achievements")
    if achievement_lines:
        _add_question(questions, f"How did you achieve the result described here: {achievement_lines[0]}?", "Achievement", "resume", [achievement_lines[0]], False, 66)
    elif achievements_info.get("performance_metrics"):
        metric = achievements_info["performance_metrics"][0]
        if _contains(resume_text, metric):
            _add_question(questions, f"What work led to the {metric} result shown on your resume?", "Achievement", "resume", [metric], False, 64)

    for skill in missing_skills or []:
        if not _contains(resume_lower, skill):
            _add_question(questions, f"The job description mentions {skill}. Do you have practical experience with it that is not currently reflected on your resume?", "JD gap", "job_description", [skill], False, 60)

    generic = [
        ("How do you approach debugging a complex issue?", "Technical", 40),
        ("Describe a time you had to learn something new quickly.", "Behavioral", 30),
        ("How do you handle conflicting requirements or priorities?", "Behavioral", 28),
    ]
    if "team" in resume_lower or "collaborat" in resume_lower:
        generic.insert(1, ("Tell me about the team or collaboration experience described on your resume.", "Behavioral", 45))
    for question, category, priority in generic:
        _add_question(questions, question, category, "generic", [], False, priority)

    questions.sort(key=lambda item: item["priority"], reverse=True)
    return questions[:15]
