from resume_evidence import build_resume_evidence
from resume_rewriter import rewrite_resume


def test_contact_and_project_content_never_become_skill_rewrites():
    resume = """SKILLS
6304676689 | email@example.com
Built a project using Python, Flask and SQL for 120 users.
Python, Flask
"""
    result = rewrite_resume(resume)
    originals = [item["original"] for item in result["rewrites"]]
    assert "6304676689 | email@example.com" not in originals
    assert "Built a project using Python, Flask and SQL for 120 users." not in originals
    assert result["rewrites"][-1]["rewritten"] == "Technical skills: Python, Flask"


def test_urls_and_bullet_content_never_become_skill_rewrites():
    resume = """TECHNICAL SKILLS
linkedin.com/in/candidate | github.com/candidate | https://example.dev
• Developed a Python, Flask, SQL booking project for 120 users.
Python, Flask
"""
    result = rewrite_resume(resume)
    rewritten = "\n".join(item["original"] for item in result["rewrites"])
    assert "linkedin.com" not in rewritten
    assert "github.com" not in rewritten
    assert "Developed a Python" not in rewritten


def test_skill_categories_keep_their_labels_and_only_normalize_formatting():
    result = rewrite_resume("SKILLS\nProgramming Languages: Python, Java, C\nTools: Python, OpenAI API, NumPy, FastAPI")
    assert result["rewrites"] == []


def test_education_content_cannot_be_rewritten_as_skills():
    resume = """SKILLS
B.Tech in Computer Science, Example University, CGPA 8.5
Python, Flask
"""
    result = rewrite_resume(resume)
    assert all("B.Tech" not in item["original"] for item in result["rewrites"])


def test_internships_and_certifications_reset_project_boundary():
    resume = """PROJECTS
Portfolio: I made a Python site.
INTERNSHIPS
AI Intern at Acme
CERTIFICATIONS
    Python Certificate
"""
    result = rewrite_resume(resume)
    assert not any(item["section"] == "project" and "Intern" in item["original"] for item in result["rewrites"])
    assert not any("Certificate" in item["original"] for item in result["rewrites"])


def test_contact_is_not_skills_evidence_when_pdf_text_merges_a_line():
    evidence = build_resume_evidence("SKILLS\nphone@example.com | 6304676689\nPython, Flask")
    assert all("@" not in item["value"] and "630467" not in item["value"] for item in evidence["skills"])


def test_extracted_ordering_case_does_not_leak_between_sections():
    # Mirrors a PDF text stream where the visible headings arrive before the
    # corresponding column content. Safety takes priority over a speculative
    # rewrite when the source order cannot establish a trustworthy boundary.
    extracted = """PROJECTS
EDUCATION
Example University, B.Tech CSE, 2025
SKILLS
Programming Languages: Python, Java, C
Tools: Python, NumPy, FastAPI
Developed an AI-powered advisory assistant, reducing manual work by 50%.
6304676689 | candidate@example.com
CERTIFICATIONS
Python Certificate
"""
    result = rewrite_resume(extracted)
    assert all(item["section"] != "skills" for item in result["rewrites"])
    assert all("Certificate" not in item["original"] for item in result["rewrites"])
    evidence = build_resume_evidence(extracted)
    assert not any("candidate@example.com" in item["value"] for item in evidence["skills"])
