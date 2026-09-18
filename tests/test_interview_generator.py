from interview_generator import generate_interview_questions


RESUME = """Candidate
SUMMARY
Backend developer
SKILLS
Python, Flask, SQL
EXPERIENCE
Python Developer Intern at Example Labs
Implemented APIs and improved response time by 30%.
PROJECTS
ResumeIQ: Flask, Python, SQL API
EDUCATION
B.Tech in Computer Science, Fictional University
CERTIFICATIONS
AWS Certified Developer
ACHIEVEMENTS
Improved response time by 30%.
"""


def generate(resume=RESUME, matched=None, missing=None, certifications=None):
    return generate_interview_questions(
        {"project_found": bool(resume)},
        {"experience_found": bool(resume)},
        {"education_found": bool(resume), "degree": "B.TECH", "branch": "Computer Science", "college": "Fictional University"},
        matched or ["python", "flask", "sql"],
        missing or [],
        "Python Flask SQL AWS role",
        resume_text=resume,
        certifications_info=certifications or {"aws_certifications": ["aws certified"]},
    )


def test_questions_use_project_and_experience_evidence():
    questions = generate()
    assert any(item["category"] == "Project" and "ResumeIQ" in item["evidence"] for item in questions)
    assert any(item["category"] == "Experience" and "Python Developer Intern" in item["evidence"][0] for item in questions)


def test_questions_use_skills_and_education_evidence():
    questions = generate()
    assert any(item["category"] == "Technical" and item["evidence"] == ["python"] for item in questions)
    assert any(item["category"] == "Education" and "B.TECH" in item["evidence"] for item in questions)


def test_questions_use_certification_evidence():
    questions = generate()
    assert any(item["category"] == "Certification" and item["source"] == "resume" for item in questions)


def test_resume_jd_matches_are_prioritized():
    questions = generate(matched=["python", "flask"], missing=[])
    assert questions[0]["source"] == "resume"
    assert questions[0]["jd_match"] is True
    assert questions[0]["priority"] >= questions[-1]["priority"]


def test_jd_only_skill_creates_safe_gap_question():
    resume = "SKILLS\nPython\nPROJECTS\nSmall Python tool"
    questions = generate(resume=resume, matched=["python"], missing=["aws"])
    gaps = [item for item in questions if item["category"] == "JD gap"]
    assert len(gaps) == 1
    assert gaps[0]["evidence"] == ["aws"]
    assert "not currently reflected" in gaps[0]["question"]
    assert not any("deploy" in item["question"].lower() and "aws" in item["question"].lower() for item in questions)


def test_resume_specific_questions_have_traceable_safe_metadata():
    questions = generate()
    resume_questions = [item for item in questions if item["source"] == "resume"]
    assert resume_questions
    assert all(item["evidence"] and item["fact_safe"] is True for item in resume_questions)
    assert all({"question", "category", "source", "evidence", "jd_match", "priority", "fact_safe"} <= set(item) for item in questions)


def test_generic_behavioral_question_does_not_claim_resume_fact():
    questions = generate(resume="SKILLS\nPython", matched=["python"])
    behavioral = [item for item in questions if item["category"] == "Behavioral"]
    assert behavioral
    assert all(item["source"] == "generic" and item["evidence"] == [] for item in behavioral)


def test_empty_resume_and_job_description_are_safe():
    questions = generate(resume="", matched=[], missing=[])
    assert questions
    assert all(item["fact_safe"] for item in questions)
    assert not any(item["source"] == "resume" for item in questions)


def test_legacy_six_argument_signature_remains_usable():
    questions = generate_interview_questions({}, {}, {}, ["python"], [], "")
    assert isinstance(questions, list)
    assert all(isinstance(item, dict) for item in questions)
