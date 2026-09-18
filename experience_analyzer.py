import re


def analyze_experience(resume_text):

    experience = {
        "experience_found": False,
        "internships": 0,
        "companies": [],
        "roles": []
    }

    text = resume_text.lower()

    # Experience keywords
    experience_words = [
        "experience",
        "intern",
        "internship",
        "worked at",
        "employment"
    ]

    for word in experience_words:

        if word in text:
            experience["experience_found"] = True
            break

    # Company names (V1)
    companies = [
        "tcs",
        "infosys",
        "wipro",
        "accenture",
        "google",
        "microsoft",
        "amazon",
        "ibm",
        "oracle"
    ]

    for company in companies:

        if company.lower() in text:
            experience["companies"].append(company.title())

    experience["internships"] = text.count("intern")

    # Roles (V1)
    roles = [
        "software engineer",
        "python developer",
        "web developer",
        "ai intern",
        "data analyst",
        "machine learning engineer"
    ]

    for role in roles:

        if role in text:
            experience["roles"].append(role.title())

    role_company_pattern = re.compile(
        r"^\s*([A-Za-z][A-Za-z /&-]{2,60}?)\s+at\s+([A-Za-z][A-Za-z0-9 &.-]{2,60})\s*$",
        re.IGNORECASE,
    )
    for line in (resume_text or "").splitlines():
        match = role_company_pattern.match(line.strip())
        if not match:
            continue
        role, company = (part.strip() for part in match.groups())
        if role.casefold() not in {item.casefold() for item in experience["roles"]}:
            experience["roles"].append(role)
        if company.casefold() not in {item.casefold() for item in experience["companies"]}:
            experience["companies"].append(company)

    return experience