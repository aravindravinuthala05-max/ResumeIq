from resume_rewriter import rewrite_resume


JD_ONLY = "Experience with Python, Flask, AWS, Docker and Kubernetes."


def test_experience_rewrite_preserves_employer_role_dates_metrics_and_technology():
    resume = "EXPERIENCE\nBackend Engineer at Acme North\n2019 - 2023\nI worked on Python APIs and improved latency by 30%."

    result = rewrite_resume(resume, JD_ONLY)

    rewrites = {item["original"]: item for item in result["rewrites"]}
    employer = rewrites["Backend Engineer at Acme North"]
    responsibility = rewrites["I worked on Python APIs and improved latency by 30%."]
    assert employer["section"] == "experience"
    assert "Backend Engineer" in employer["rewritten"]
    assert "Acme North" in employer["rewritten"]
    assert "2019" not in employer["rewritten"]
    assert "Python" in responsibility["rewritten"]
    assert "30%" in responsibility["rewritten"]
    assert "AWS" not in responsibility["rewritten"]
    assert "Docker" not in responsibility["rewritten"]
    assert "Kubernetes" not in responsibility["rewritten"]
    assert result["fact_safe"] is True


def test_project_rewrites_keep_project_specific_technologies_and_metrics_separate():
    resume = """PROJECTS
Inventory Tool: I made a Python Flask tool for 120 users.
Billing Service: I used Java and SQL for invoice processing.
"""

    result = rewrite_resume(resume, "Python Flask Java SQL AWS")
    rewrites = {item["original"]: item for item in result["rewrites"]}

    inventory = rewrites["Inventory Tool: I made a Python Flask tool for 120 users."]
    billing = rewrites["Billing Service: I used Java and SQL for invoice processing."]
    assert inventory["section"] == "project"
    assert billing["section"] == "project"
    assert "Python" in inventory["rewritten"]
    assert "Flask" in inventory["rewritten"]
    assert "120 users" in inventory["rewritten"]
    assert "Java" not in inventory["rewritten"]
    assert "Java" in billing["rewritten"]
    assert "SQL" in billing["rewritten"]
    assert "Python" not in billing["rewritten"]
    assert all(item["fact_safe"] for item in result["rewrites"])


def test_skills_rewrite_only_formats_resume_supported_skills():
    result = rewrite_resume("SKILLS\nPython, Flask", JD_ONLY)

    item = result["rewrites"][0]
    assert item["original"] == "Python, Flask"
    assert item["rewritten"] == "Technical skills: Python, Flask"
    assert all(skill not in item["rewritten"] for skill in ("AWS", "Docker", "Kubernetes"))
    assert set(result["missing_keywords"]) >= {"aws", "docker", "kubernetes"}


def test_education_rewrite_preserves_degree_institution_and_date():
    result = rewrite_resume(
        "EDUCATION\nB.Sc. Computer Science, Northbridge University, 2025",
        "Python AWS",
    )

    item = result["rewrites"][0]
    assert item["section"] == "education"
    assert item["original"] == "B.Sc. Computer Science, Northbridge University, 2025"
    assert item["rewritten"] == "B.Sc. Computer Science | Northbridge University | 2025"
    assert "Northbridge University" in item["rewritten"]
    assert "2025" in item["rewritten"]
    assert "B.Sc." in item["rewritten"]


def test_certifications_and_achievements_keep_existing_no_candidate_state():
    certification = rewrite_resume("CERTIFICATIONS\nAcme Cloud Associate, 2024", "Python AWS")
    achievement = rewrite_resume("ACHIEVEMENTS\nReduced costs by 25% in 2023.", "Python AWS")

    assert certification["rewrites"] == []
    assert achievement["rewrites"] == []
    assert "No supported rewrite candidates" in certification["message"]
    assert "No supported rewrite candidates" in achievement["message"]


def test_multi_section_rewrites_keep_original_text_and_source_section():
    resume = """SUMMARY
I worked on reliable APIs.
EXPERIENCE
I worked on services at Acme North.
PROJECTS
I made a Python Flask project.
SKILLS
Python, Flask, SQL
"""

    result = rewrite_resume(resume, "Python Flask SQL AWS")
    assert [(item["section"], item["original"]) for item in result["rewrites"]] == [
        ("summary", "I worked on reliable APIs."),
        ("experience", "I worked on services at Acme North."),
        ("project", "I made a Python Flask project."),
        ("skills", "Python, Flask, SQL"),
    ]
    assert "Python" not in result["rewrites"][0]["rewritten"]
    assert "Acme North" in result["rewrites"][1]["rewritten"]
    assert "Flask" in result["rewrites"][2]["rewritten"]
    assert "AWS" not in " ".join(item["rewritten"] for item in result["rewrites"])


def test_clear_section_keeps_existing_no_change_behavior():
    result = rewrite_resume("SUMMARY\nExperienced Python developer.", "Python AWS")

    assert result["rewrites"] == []
    assert "No supported rewrite candidates" in result["message"]


def test_exact_jd_only_safety_example_never_claims_missing_technologies():
    result = rewrite_resume("PROJECTS\nBuilt a Python Flask application.", JD_ONLY)
    rewritten = " ".join(item["rewritten"] for item in result["rewrites"])

    assert "AWS" not in rewritten
    assert "Docker" not in rewritten
    assert "Kubernetes" not in rewritten
    assert result["fact_safe"] is True
