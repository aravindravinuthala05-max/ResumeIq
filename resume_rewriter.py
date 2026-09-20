"""Provider-independent, fact-preserving resume rewriting."""

import re
from abc import ABC, abstractmethod

from ats_engine import calculate_ats_score
from achievement_analyzer import analyze_achievements
from certification_analyzer import analyze_certifications
from education_analyzer import analyze_education
from experience_analyzer import analyze_experience
from language_analyzer import analyze_languages
from resume_sections import SECTION_ALIASES as ALL_SECTION_ALIASES, extract_section_lines, is_contact_line, normalize_heading, section_for_heading


SECTION_ALIASES = {"project" if key == "projects" else key: value for key, value in ALL_SECTION_ALIASES.items()}

ACTION_REPLACEMENTS = (
    (r"\bworked on\b", "contributed to"),
    (r"\bhelped with\b", "supported"),
    (r"\bhelped\b", "supported"),
    (r"\bresponsible for\b", "managed"),
    (r"\bused\b", "applied"),
    (r"\bmade\b", "created"),
    (r"\bdid\b", "executed"),
)

SUPPORTED_SECTIONS = ("summary", "experience", "project", "skills", "education")
FACTUAL_TECHNOLOGIES = {
    "aws", "azure", "gcp", "docker", "kubernetes", "python", "java", "javascript",
    "typescript", "c++", "c#", "ruby", "php", "go", "rust", "kotlin", "swift",
    "flask", "django", "fastapi", "react", "angular", "node.js", "nodejs", "sql",
    "mysql", "postgresql", "mongodb", "redis", "tensorflow", "pytorch", "opencv",
    "pandas", "numpy", "git", "github", "html", "css", "linux", "jenkins", "terraform",
}
FACTUAL_COMPANIES = {"google", "microsoft", "amazon", "ibm", "oracle", "tcs", "infosys", "wipro", "accenture"}
FACTUAL_DEGREES = {"b.tech", "btech", "bachelor", "bachelor of technology", "m.tech", "mtech", "b.sc", "bsc", "m.sc", "msc", "bca", "mca"}


class RewriteProvider(ABC):
    """Interface for a future LLM provider and the local fallback."""

    name = "provider"

    @abstractmethod
    def rewrite(self, resume_text, job_description="", analysis=None):
        """Return a fact-safe structured rewrite response."""


class RuleBasedRewriteProvider(RewriteProvider):
    """Deterministic fallback that changes wording without adding facts."""

    name = "rule_based"

    def rewrite(self, resume_text, job_description="", analysis=None):
        sections = _extract_sections(resume_text)
        analysis = analysis or {}
        matched_skills, missing_skills = _skill_context(resume_text, job_description, analysis)
        evidence = _build_evidence(resume_text, analysis, matched_skills, missing_skills)
        rewrites = []

        for section, lines in sections.items():
            for line in lines:
                improved = _rewrite_line(line, section)
                if section == "skills":
                    improved = _rewrite_skills(line)
                if section == "education":
                    improved = _rewrite_education(line)
                if not improved or improved == line:
                    continue
                keyword_evidence = _keyword_evidence(line, resume_text, matched_skills, missing_skills, evidence)
                rewrites.append({
                    "section": section,
                    "original": line,
                    "rewritten": improved,
                    "reason": _reason_for(section),
                    "keywords": [item["keyword"] for item in keyword_evidence if item["status"] == "supported"],
                    "keyword_evidence": keyword_evidence,
                    "fact_safe": True,
                    "safety_issues": [],
                    "provider": self.name,
                })

        return {
            "provider": self.name,
            "mode": "deterministic_fallback",
            "rewrites": rewrites,
            "missing_keywords": [
                skill for skill in missing_skills
                if not _contains_skill(resume_text, skill)
            ],
            "keyword_evidence": [
                item for item in evidence
                if item["keyword"] in missing_skills or item["status"] == "supported"
            ],
            "message": (
                "These wording improvements use only facts already present in the resume. "
                "No external AI provider is configured."
            ) if rewrites else "No supported rewrite candidates were found in the resume.",
        }


def _normalize_heading(line):
    return re.sub(r"[^a-z ]", "", line.lower()).strip()


def _section_for_heading(line):
    normalized = _normalize_heading(line)
    for section, aliases in SECTION_ALIASES.items():
        if normalized in aliases:
            return section
    return None


def _extract_sections(resume_text):
    sections = {section: [] for section in SUPPORTED_SECTIONS}
    for section, lines in extract_section_lines(resume_text).items():
        target = "project" if section == "projects" else section
        if target in sections:
            sections[target].extend(line for line in lines if not is_contact_line(line))
    return sections


def _looks_like_heading(line):
    normalized = _normalize_heading(line)
    return any(normalized in aliases for aliases in SECTION_ALIASES.values())


def _rewrite_line(line, section):
    rewritten = line.strip()
    for pattern, replacement in ACTION_REPLACEMENTS:
        rewritten = re.sub(pattern, replacement, rewritten, flags=re.IGNORECASE)
    rewritten = re.sub(r"\s+", " ", rewritten)
    if rewritten and rewritten[0].islower():
        rewritten = rewritten[0].upper() + rewritten[1:]
    if section in {"experience", "project"} and rewritten and not rewritten.endswith((".", "!", "?")):
        rewritten += "."
    return rewritten


def _rewrite_skills(line):
    if is_contact_line(line):
        return line.strip()
    category, separator, values = line.partition(":")
    if separator and _is_skill_category(category) and _is_skill_values(values):
        return f"{category.strip()}: {', '.join(part.strip() for part in re.split(r'[,;|]', values) if part.strip())}"
    if not _is_skill_values(line):
        return line.strip()
    parts = [part.strip() for part in re.split(r"[,;|]", line) if part.strip()]
    if len(parts) < 2:
        return line.strip()
    return "Technical skills: " + ", ".join(parts)


def _is_skill_category(value):
    return bool(re.fullmatch(r"(?:programming )?languages?|databases?|libraries?|frameworks?|tools?|cloud|data science(?: & ml)?|data visualization(?: & analytics)?|web development|technologies?|technical expertise", value.strip(), re.IGNORECASE))


def _is_skill_values(value):
    text = value.strip()
    if not text or is_contact_line(text) or re.search(r"\b(?:developed|implemented|worked|built|improved|completed|achieved|reducing|experience|project|internship)\b", text, re.IGNORECASE):
        return False
    parts = [part.strip() for part in re.split(r"[,;|]", text) if part.strip()]
    known_skill = re.compile(r"\b(?:python|java|c\+\+|c#|sql|aws|azure|gcp|docker|kubernetes|react|angular|flask|django|fastapi|pandas|numpy|pytorch|tensorflow|html|css|javascript|typescript|git|excel|matplotlib|scikit-?learn|openai api|jupyter|visual studio code)\b", re.IGNORECASE)
    if len(parts) == 1:
        return bool(known_skill.search(text))
    return all(len(part.split()) <= 4 and bool(known_skill.search(part)) for part in parts)


def _rewrite_education(line):
    if not _looks_like_education(line):
        return line.strip()
    parts = [part.strip() for part in line.split(",") if part.strip()]
    if len(parts) < 2:
        return line.strip()
    return " | ".join(parts)


def _looks_like_education(line):
    return bool(re.search(r"\b(?:b\.?\s?(?:tech|sc|e|ca)|m\.?\s?(?:tech|sc|ca)|bachelor|master|college|university|school|cgpa|gpa|ssc|intermediate)\b", line, re.IGNORECASE))


def _reason_for(section):
    return {
        "summary": "Improves clarity and professional tone while preserving the source wording.",
        "experience": "Uses stronger action wording and concise sentence structure without adding facts.",
        "project": "Makes the project statement clearer and more professional without adding facts.",
        "skills": "Organizes the existing skills into a clearer ATS-readable phrase.",
        "education": "Improves readability while preserving the original education details.",
    }[section]


def _build_evidence(resume_text, analysis, matched_skills, missing_skills):
    analyzer_data = {
        "experience": analyze_experience(resume_text),
        "education": analyze_education(resume_text),
        "certifications": analyze_certifications(resume_text),
        "achievements": analyze_achievements(resume_text),
        "languages": analyze_languages(resume_text),
    }
    records = []
    for skill in matched_skills:
        if _contains_skill(resume_text, skill):
            records.append({
                "keyword": skill,
                "status": "supported",
                "source": _source_for_keyword(resume_text, skill),
            })
    for skill in missing_skills:
        supported = _contains_skill(resume_text, skill)
        records.append({
            "keyword": skill,
            "status": "supported" if supported else "unsupported",
            "source": _source_for_keyword(resume_text, skill) if supported else "none",
        })

    for section, values in analyzer_data.items():
        for value in _evidence_values(values):
            if isinstance(value, str) and value not in {item["keyword"] for item in records}:
                records.append({
                    "keyword": value,
                    "status": "supported",
                    "source": section,
                })
    for item in (analysis or {}).get("resume_evidence", {}).get("technologies", []):
        keyword = item.get("value")
        if not keyword or any(record["keyword"].casefold() == keyword.casefold() for record in records):
            continue
        records.append({
            "keyword": keyword,
            "status": "supported",
            "source": item.get("section", "resume"),
        })
    return records


def _evidence_values(value):
    if isinstance(value, dict):
        values = []
        for key, item in value.items():
            if key in {"degree", "branch", "college", "performance_metrics", "impact_keywords", "companies", "roles", "programming_languages", "markup_languages", "scripting_languages", "natural_languages"}:
                values.extend(_evidence_values(item))
        return values
    if isinstance(value, (list, tuple)):
        return [item for nested in value for item in _evidence_values(nested)]
    if isinstance(value, str) and value not in {"Not Found", ""}:
        return [value]
    return []


def _source_for_keyword(resume_text, keyword):
    for section, lines in _extract_sections(resume_text).items():
        if any(_contains_skill(line, keyword) for line in lines):
            return section
    return "resume"


def _keyword_evidence(line, resume_text, matched_skills, missing_skills, evidence):
    records = []
    for item in evidence:
        keyword = item["keyword"]
        if _contains_skill(line, keyword) and item["status"] == "supported":
            records.append({
                "keyword": keyword,
                "status": "supported",
                "source": item["source"] or _source_for_keyword(resume_text, keyword),
            })
    return records


def _contains_skill(text, skill):
    phrase = skill.split(" (", 1)[0]
    return bool(re.search(r"(?<!\w)" + re.escape(phrase.lower()) + r"(?!\w)", text.lower()))


def _skill_context(resume_text, job_description, analysis):
    matched = analysis.get("matched_skills") if isinstance(analysis, dict) else None
    missing = analysis.get("missing_skills") if isinstance(analysis, dict) else None
    if matched is None or missing is None:
        _, matched, missing = calculate_ats_score(resume_text, job_description)
    return matched or [], missing or []


def _supported_keywords(line, matched_skills):
    return [skill for skill in matched_skills if _contains_skill(line, skill)]


def _factual_tokens(text):
    lowered = text.lower()
    tokens = set(re.findall(r"\b(?:19|20)\d{2}\b|\b\d+(?:\.\d+)?%?\b", text))
    tokens.update(technology for technology in FACTUAL_TECHNOLOGIES if _contains_skill(lowered, technology))
    tokens.update(company for company in FACTUAL_COMPANIES if _contains_skill(lowered, company))
    tokens.update(degree for degree in FACTUAL_DEGREES if _contains_skill(lowered, degree))
    if "certif" in lowered:
        tokens.add("certification")
    return tokens


def _validate_fact_safety(original, rewritten):
    original_tokens = _factual_tokens(original)
    rewritten_tokens = _factual_tokens(rewritten)
    unsupported = sorted(rewritten_tokens - original_tokens)
    return not unsupported, unsupported


def _enforce_fact_safety(response, resume_text):
    for item in response.get("rewrites", []):
        safe, issues = _validate_fact_safety(item.get("original", ""), item.get("rewritten", ""))
        if safe:
            item["fact_safe"] = True
            item["safety_issues"] = []
            continue
        item["rewritten"] = item.get("original", "")
        item["fact_safe"] = False
        item["safety_issues"] = issues
        item["reason"] = "Kept the original wording because the proposed change introduced unsupported factual content."
    response["fact_safe"] = all(item.get("fact_safe") is True for item in response.get("rewrites", []))
    return response


def rewrite_resume(resume_text, job_description="", analysis=None, provider=None):
    """Rewrite existing resume wording using a safe provider.

    The default provider is deterministic and local. A future provider can be
    supplied without changing the endpoint or response contract.
    """
    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("resume_text must be a non-empty string")
    if job_description is not None and not isinstance(job_description, str):
        raise ValueError("job_description must be a string")
    selected_provider = provider or RuleBasedRewriteProvider()
    response = selected_provider.rewrite(resume_text, job_description or "", analysis)
    return _enforce_fact_safety(response, resume_text)
