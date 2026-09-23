"""Narrow deterministic extraction of explicit JD eligibility requirements."""
import re

DEGREE_ALIASES = {"b.tech": "btech", "bachelor of technology": "btech", "b.e.": "be", "bachelor of engineering": "be", "m.tech": "mtech", "m.e.": "me", "mca": "mca", "bca": "bca"}
BRANCH_ALIASES = {"computer science": "computer_science", "computer science and engineering": "computer_science", "cse": "computer_science", "artificial intelligence and machine learning": "aiml", "aiml": "aiml", "information technology": "information_technology", "it": "information_technology"}

def _item(kind, text, value=None, unit=None):
    return {"requirement_type": kind, "original_requirement_text": text.strip(), "normalized_requirement": kind.lower(), "value": value, "unit": unit, "source": "job_description"}

def extract_eligibility_requirements(job_description):
    text = job_description or ""; found = []
    def add(item):
        if item not in found: found.append(item)
    for match in re.finditer(r"(?:minimum|min\.?|at least)\s*(?:cgpa(?:\s+of)?|gpa(?:\s+of)?)\s*(\d(?:\.\d+)?)", text, re.I): add(_item("MIN_CGPA", match.group(), float(match.group(1)), "cgpa"))
    for match in re.finditer(r"(?:minimum|min\.?|at least)\s*(\d{2,3}(?:\.\d+)?)\s*%\s*(?:marks?|percentage|academics?|in (?:10th|12th|degree))", text, re.I): add(_item("MIN_PERCENTAGE", match.group(), float(match.group(1)), "percentage"))
    for match in re.finditer(r"(?:graduating in|graduates? (?:of|in)|graduation year\s*[:=-]?)\s*(20\d{2})", text, re.I): add(_item("GRADUATION_YEAR", match.group(), int(match.group(1)), "year"))
    for match in re.finditer(r"(?:maximum|max\.?|up to)\s*(\d+)\s*active backlogs?", text, re.I): add(_item("MAX_ACTIVE_BACKLOGS", match.group(), int(match.group(1)), "backlogs"))
    for match in re.finditer(r"(?:minimum|min\.?|at least)\s*(\d+(?:\.\d+)?)\s*(years?|months?)\s+(?:of )?experience", text, re.I): add(_item("MIN_EXPERIENCE", match.group(), float(match.group(1)), match.group(2).lower()))
    for alias, normalized in DEGREE_ALIASES.items():
        if re.search(r"(?:required|must have|eligible|degree|qualification).*\b" + re.escape(alias) + r"\b|\b" + re.escape(alias) + r"\b.*(?:required|degree|qualification)", text, re.I): add(_item("DEGREE", alias, normalized))
    for alias, normalized in BRANCH_ALIASES.items():
        if re.search(r"(?:branch|discipline|degree|qualification|required).*\b" + re.escape(alias) + r"\b", text, re.I): add(_item("BRANCH", alias, normalized))
    for match in re.finditer(r"\b([A-Za-z0-9 .-]+(?:certified|certification|certificate))\s+(?:is\s+)?required\b|\b(required)\s*:\s*([A-Za-z0-9 .-]+(?:certification|certificate))", text, re.I): add(_item("CERTIFICATION", match.group(), (match.group(1) or match.group(3)).strip().casefold()))
    if re.search(r"\b(?:authorized to work|work authorization|eligible to work)\b", text, re.I): add(_item("WORK_AUTHORIZATION", re.search(r"[^.]*\b(?:authorized to work|work authorization|eligible to work)\b[^.]*", text, re.I).group()))
    return found
