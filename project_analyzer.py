def analyze_projects(resume_text):

    projects = {
        "project_found": False,
        "total_projects": 0,
        "ai_projects": 0,
        "web_projects": 0,
        "mobile_projects": 0,
        "iot_projects": 0
    }

    text = resume_text.lower()

    # Project Section
    if "project" in text or "projects" in text:
        projects["project_found"] = True

    # Count project keyword
    projects["total_projects"] = text.count("project")

    # AI Projects
    ai_keywords = [
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "tensorflow",
        "opencv",
        "nlp"
    ]

    for keyword in ai_keywords:
        if keyword in text:
            projects["ai_projects"] += 1

    # Web Projects
    web_keywords = [
        "flask",
        "django",
        "react",
        "html",
        "css",
        "javascript"
    ]

    for keyword in web_keywords:
        if keyword in text:
            projects["web_projects"] += 1

    # Mobile Projects
    mobile_keywords = [
        "android",
        "flutter",
        "kotlin"
    ]

    for keyword in mobile_keywords:
        if keyword in text:
            projects["mobile_projects"] += 1

    # IoT Projects
    iot_keywords = [
        "raspberry pi",
        "arduino",
        "iot"
    ]

    for keyword in iot_keywords:
        if keyword in text:
            projects["iot_projects"] += 1

    return projects