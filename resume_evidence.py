"""Deterministic, traceable evidence extracted from an uploaded resume."""

import re


SECTION_ALIASES = {
    "summary": {"summary", "professional summary", "profile", "objective"},
    "experience": {"experience", "work experience", "employment", "professional experience"},
    "projects": {"project", "projects", "personal projects", "academic projects"},
    "skills": {"skill", "skills", "technical skills", "technologies", "technical expertise"},
    "education": {"education", "academic background"},
    "certifications": {"certification", "certifications", "certificates"},
    "achievements": {"achievement", "achievements", "awards"},
    "languages": {"languages", "programming languages"},
}

TECHNOLOGY_TYPES = {
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "ruby", "php", "go", "rust",
    "kotlin", "swift", "flask", "django", "fastapi", "react", "angular", "node.js", "nodejs",
    "sql", "mysql", "postgresql", "mongodb", "redis", "aws", "azure", "gcp", "docker",
    "kubernetes", "jenkins", "terraform", "tensorflow", "pytorch", "opencv", "pandas", "numpy",
    "git", "github", "html", "css", "linux", "rest api", "machine learning", "deep learning",
    "scikit-learn", "scikit learn", "spring boot", "android", "flutter", "arduino", "iot",
}

METRIC_PATTERN = re.compile(
    r"(?<!\w)(?:\$\d+(?:\.\d+)?[KMB]?|\d+(?:\.\d+)?%|\d+(?:\.\d+)?\+?\s+"
    r"(?:users?|clients?|downloads?|projects?|ms|seconds?|minutes?|hours?|days?|weeks?|months?|years?|"
    r"thousand|million|billion)|"
    r"\d+(?:\.\d+)?x)(?!\w)",
    re.IGNORECASE,
)
DATE_PATTERN = re.compile(
    r"\b(?:19|20)\d{2}\b|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(?:19|20)\d{2}\b",
    re.IGNORECASE,
)


def _clean_lines(resume_text):
    return [line.strip() for line in (resume_text or "").splitlines() if line.strip()]


def _heading(line):
    return re.sub(r"[^a-z ]", "", line.lower()).strip()


def _section_lines(resume_text):
    sections = {section: [] for section in SECTION_ALIASES}
    current = None
    for line in _clean_lines(resume_text):
        normalized = _heading(line)
        found = next((section for section, aliases in SECTION_ALIASES.items() if normalized in aliases), None)
        if found:
            current = found
            continue
        if current:
            sections[current].append(line)
    return sections


def _contains(text, value):
    return bool(re.search(r"(?<!\w)" + re.escape(str(value).lower()) + r"(?!\w)", str(text).lower()))


def _unique(values):
    result = []
    seen = set()
    for value in values:
        normalized = str(value).strip()
        key = normalized.casefold()
        if normalized and key not in seen:
            seen.add(key)
            result.append(normalized)
    return result


def _record(value, evidence_type, section, source_text, source):
    return {
        "value": str(value).strip(),
        "type": evidence_type,
        "section": section,
        "source_text": str(source_text).strip(),
        "source": source,
    }


def _records(values, evidence_type, section, source_text, source):
    return [_record(value, evidence_type, section, source_text, source) for value in _unique(values)]


def _analyzer_value(analyzer_data, key):
    value = (analyzer_data or {}).get(key)
    return value if value not in (None, "", "Not Found") else None


def _technology_records(resume_text, sections, languages_info):
    records = []
    candidates = []
    for key in ("programming_languages", "markup_languages", "scripting_languages"):
        candidates.extend((languages_info or {}).get(key, []))
    for candidate in TECHNOLOGY_TYPES:
        candidates.append(candidate)
    for candidate in _unique(candidates):
        for section in ("skills", "projects", "experience", "summary"):
            source_text = next((line for line in sections[section] if _contains(line, candidate)), None)
            if source_text:
                records.append(_record(candidate, "technology", section, source_text, "resume_evidence"))
                break
    return records


def build_resume_evidence(
    resume_text,
    *,
    education=None,
    experience=None,
    projects=None,
    certifications=None,
    achievements=None,
    languages=None,
    contact=None,
):
    """Build JSON-safe evidence records from resume text and existing analyzers.

    Analyzer arguments are optional so this module remains independent from Flask
    and can be used directly in focused tests or future consumers.
    """
    resume_text = resume_text or ""
    sections = _section_lines(resume_text)
    evidence = {key: [] for key in (
        "summary", "experience", "projects", "skills", "education", "certifications",
        "achievements", "languages", "technologies", "metrics", "dates",
    )}

    for line in sections["summary"]:
        evidence["summary"].append(_record(line, "summary", "summary", line, "resume"))

    for line in sections["projects"]:
        name, separator, details = line.partition(":")
        project_name = name.strip() if separator else line.strip()
        evidence["projects"].append(_record(project_name, "project", "projects", line, "project_analyzer"))
        if separator and details.strip():
            evidence["projects"].append(_record(details.strip(), "project_detail", "projects", line, "resume"))

    experience_values = []
    for key in ("companies", "roles"):
        experience_values.extend((experience or {}).get(key, []))
    for value in _unique(experience_values):
        source_text = next((line for line in sections["experience"] if _contains(line, value)), value)
        if _contains(resume_text, value):
            evidence["experience"].append(_record(value, "company" if value in (experience or {}).get("companies", []) else "job_title", "experience", source_text, "experience_analyzer"))
    for line in sections["experience"]:
        if not any(item["source_text"] == line for item in evidence["experience"]):
            evidence["experience"].append(_record(line, "experience_detail", "experience", line, "resume"))

    education_values = []
    for key, evidence_type in (("degree", "degree"), ("branch", "specialization"), ("college", "institution"), ("cgpa", "grade")):
        value = _analyzer_value(education, key)
        if value and _contains(resume_text, value):
            source_text = next((line for line in sections["education"] if _contains(line, value)), value)
            if evidence_type == "institution":
                value = next((part.strip() for part in source_text.split(",") if re.search(r"\b(?:college|university|institute)\b", part, re.IGNORECASE)), value)
            evidence["education"].append(_record(value, evidence_type, "education", source_text, "education_analyzer"))
    for line in sections["education"]:
        if not any(item["source_text"] == line for item in evidence["education"]):
            evidence["education"].append(_record(line, "education_detail", "education", line, "resume"))

    certification_values = []
    for key in ("aws_certifications", "gcp_certifications", "azure_certifications", "other_certifications"):
        certification_values.extend((certifications or {}).get(key, []))
    for line in sections["certifications"]:
        evidence["certifications"].append(_record(line, "certification", "certifications", line, "resume"))
    for value in _unique(certification_values):
        if value.casefold() in {"certified", "certification"}:
            continue
        if _contains(resume_text, value) and not any(item["value"].casefold() == value.casefold() for item in evidence["certifications"]):
            evidence["certifications"].append(_record(value, "certification", "certifications", value, "certification_analyzer"))

    for line in sections["achievements"]:
        evidence["achievements"].append(_record(line, "achievement", "achievements", line, "resume"))

    language_values = []
    for key in ("programming_languages", "markup_languages", "scripting_languages", "natural_languages"):
        language_values.extend((languages or {}).get(key, []))
    evidence["languages"].extend(_records(language_values, "language", "languages", "\n".join(sections["languages"]) or resume_text, "language_analyzer"))
    for line in sections["skills"]:
        skills = [part.strip() for part in re.split(r"[,;|]", line) if part.strip()]
        evidence["skills"].extend(_records(skills, "skill", "skills", line, "resume"))
    evidence["technologies"] = _technology_records(resume_text, sections, languages)

    metric_records = []
    date_records = []
    for line in _clean_lines(resume_text):
        metric_records.extend(_records(METRIC_PATTERN.findall(line), "metric", "resume", line, "resume"))
        date_records.extend(_records(DATE_PATTERN.findall(line), "date", "resume", line, "resume"))
    evidence["metrics"] = metric_records
    evidence["dates"] = date_records
    return evidence
