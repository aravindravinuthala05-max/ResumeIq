"""Small, shared safeguards for heading-aware resume consumers."""

import re


SECTION_ALIASES = {
    "summary": {"summary", "professional summary", "profile", "objective"},
    "experience": {"experience", "work experience", "employment", "professional experience", "internships", "internship", "work history", "career history", "professional history"},
    "projects": {"project", "projects", "academic projects", "personal projects", "selected work", "portfolio"},
    "skills": {"skill", "skills", "technical skills", "technologies", "technical expertise", "technical toolkit", "core competencies", "tools"},
    "education": {"education", "academic background", "academic history"},
    "certifications": {"certification", "certifications", "certificates"},
    "achievements": {"achievement", "achievements", "awards"},
    "languages": {"languages"},
}

CONTACT_PATTERN = re.compile(
    r"(?:\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|"
    r"(?:\+?\d[\d .()-]{7,}\d)|"
    r"(?:https?://|www\.)\S+|(?:linkedin|github)\.com(?:/|\b))", re.IGNORECASE
)


def clean_lines(text):
    return [line.strip() for line in (text or "").splitlines() if line.strip()]


def normalize_heading(line):
    """Only normalize punctuation; a complete line must still match an alias."""
    return re.sub(r"[^a-z ]", "", line.lower()).strip()


def section_for_heading(line):
    normalized = normalize_heading(line)
    return next((name for name, aliases in SECTION_ALIASES.items() if normalized in aliases), None)


def is_contact_line(line):
    return bool(CONTACT_PATTERN.search(line or ""))


def extract_section_lines(text):
    """Return body lines only, resetting at every recognized heading.

    Resetting at unsupported headings (certifications, achievements and languages)
    is intentional: it prevents their content leaking into the last rewriteable
    section.
    """
    sections = {name: [] for name in SECTION_ALIASES}
    current = None
    for line in clean_lines(text):
        heading = section_for_heading(line)
        if heading:
            current = heading
            continue
        if current:
            sections[current].append(line)
    return sections
