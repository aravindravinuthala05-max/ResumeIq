import re


def analyze_education(resume_text):

    education = {
        "education_found": False,
        "degree": "Not Found",
        "branch": "Not Found",
        "college": "Not Found",
        "cgpa": "Not Found"
    }

    text = resume_text.lower()

    # -------- Degree --------

    degrees = [
        "b.tech",
        "btech",
        "bachelor of technology",
        "b.e",
        "be",
        "m.tech",
        "mtech",
        "b.sc",
        "bsc",
        "m.sc",
        "msc",
        "bca",
        "mca"
    ]

    for degree in degrees:
        if degree in text:
            education["degree"] = degree.upper()
            education["education_found"] = True
            break

    # -------- Branch --------

    branches = [
        "computer science",
        "artificial intelligence",
        "machine learning",
        "information technology",
        "electronics",
        "electrical",
        "mechanical",
        "civil"
    ]

    for branch in branches:
        if branch in text:
            education["branch"] = branch.title()
            break

    # -------- CGPA --------

    cgpa = re.search(r'\b\d\.\d{1,2}\b', resume_text)

    if cgpa:
        education["cgpa"] = cgpa.group()

    # -------- College --------

    college_keywords = [
        "college",
        "university",
        "institute"
    ]

    lines = resume_text.split("\n")

    for line in lines:

        for keyword in college_keywords:

            if keyword.lower() in line.lower():

                education["college"] = line.strip()

                break

    return education