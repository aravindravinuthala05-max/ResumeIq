def detect_resume_sections(resume_text):

    resume_text = resume_text.lower()

    sections = {
        "Education": False,
        "Experience": False,
        "Projects": False,
        "Skills": False,
        "Certifications": False
    }

    education_keywords = [
        "education",
        "academic background",
        "academic history",
        "b.tech",
        "btech",
        "bachelor",
        "degree",
        "university",
        "college"
    ]

    experience_keywords = [
        "experience",
        "work history",
        "professional history",
        "career history",
        "internship",
        "intern",
        "work experience",
        "employment"
    ]

    project_keywords = [
        "projects",
        "project",
        "selected work",
        "portfolio",
        "academic project"
    ]

    skill_keywords = [
        "skills",
        "technical skills",
        "technologies",
        "tools",
        "technical toolkit",
        "core competencies"
    ]

    certification_keywords = [
        "certifications",
        "certification",
        "certificate"
    ]

    for word in education_keywords:
        if word in resume_text:
            sections["Education"] = True
            break

    for word in experience_keywords:
        if word in resume_text:
            sections["Experience"] = True
            break

    for word in project_keywords:
        if word in resume_text:
            sections["Projects"] = True
            break

    for word in skill_keywords:
        if word in resume_text:
            sections["Skills"] = True
            break

    for word in certification_keywords:
        if word in resume_text:
            sections["Certifications"] = True
            break

    return sections