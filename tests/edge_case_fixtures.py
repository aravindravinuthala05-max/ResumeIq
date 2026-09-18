"""Small realistic resume and job-description fixtures for edge-case coverage."""

EDGE_CASES = [
    {
        "name": "student_resume",
        "resume": """Ava Student
ava.student@example.com
EDUCATION
B.Sc. Computer Science, Northbridge University, 2025
PROJECTS
Campus Planner: Python, Flask, SQLite
Built a scheduling tool for 200 students.
SKILLS
Python, Flask, SQL, Git
""",
        "job_description": "Junior Python developer with Flask, SQL, Git, and Docker.",
        "sections": {"Education", "Projects", "Skills"},
    },
    {
        "name": "experienced_multiple_employers",
        "resume": """Morgan Engineer
morgan@example.com
SUMMARY
Backend engineer with seven years of API experience.
EXPERIENCE
Senior Engineer at Northwind Systems
2019 - 2024
Led Python services and mentored engineers.
Software Engineer at Blue Oak Labs
2016 - 2019
Built Java and SQL reporting tools.
SKILLS
Python, Java, SQL, Docker
""",
        "job_description": "Backend engineer with Python, Java, SQL, Docker, and Kubernetes.",
        "sections": {"Experience", "Skills"},
    },
    {
        "name": "projects_without_work_experience",
        "resume": """Riley Builder
riley@example.com
EDUCATION
BCA, Lakeside College
PROJECTS
Budget Board: JavaScript, React
Created a budgeting dashboard for student groups.
Open Notes: Python, Flask
Published a searchable notes application.
SKILLS
JavaScript, React, Python, Flask
""",
        "job_description": "Frontend developer with React, JavaScript, TypeScript, and AWS.",
        "sections": {"Education", "Projects", "Skills"},
    },
    {
        "name": "work_without_projects",
        "resume": """Taylor Operator
taylor@example.com
EXPERIENCE
Support Engineer at Harbor Data
2020 - 2024
Resolved customer issues and automated support workflows.
SKILLS
Python, Linux, Git
EDUCATION
Information Systems, Westfield University
""",
        "job_description": "Support engineer with Python, Linux, Git, and Terraform.",
        "sections": {"Experience", "Skills", "Education"},
    },
    {
        "name": "certified_candidate",
        "resume": """Casey Cloud
casey@example.com
CERTIFICATIONS
AWS Certified Developer - Associate, 2023
Microsoft Azure Fundamentals, 2024
SKILLS
Python, AWS, Azure
EXPERIENCE
Cloud Engineer at Cedar Works
2022 - 2024
Automated cloud deployment checks.
""",
        "job_description": "Cloud engineer with AWS, Azure, Terraform, and Python.",
        "sections": {"Certifications", "Skills", "Experience"},
    },
    {
        "name": "achievement_focused",
        "resume": """Jordan Results
jordan@example.com
ACHIEVEMENTS
Reduced build time by 40%.
Won the 2022 regional coding challenge.
Increased test coverage to 92% across two services.
SKILLS
Python, pytest, Git
EXPERIENCE
Developer at Meridian Apps
2021 - 2023
Improved release automation.
""",
        "job_description": "Python developer with Git, testing, and CI/CD experience.",
        "sections": {"Skills", "Experience"},
    },
    {
        "name": "no_summary",
        "resume": """Sam Direct
sam@example.com
SKILLS
Python, SQL, Flask
EXPERIENCE
Developer at Plainview
2021 - 2023
Maintained internal APIs.
EDUCATION
B.Tech Computer Science, East University
""",
        "job_description": "Python Flask engineer with SQL and AWS.",
        "sections": {"Skills", "Experience", "Education"},
    },
    {
        "name": "unusual_headings",
        "resume": """Lee Structured
lee@example.com
ACADEMIC BACKGROUND
B.Sc. Software Engineering, Summit University
WORK HISTORY
Developer at Signal Labs
2021 - 2024
Maintained Python services.
SELECTED WORK
Inventory Tool: Python, Flask
TOOLS
Python, Flask, Git
AWARDS
Received a 2023 engineering award.
""",
        "job_description": "Python Flask developer with Git and Docker.",
        "sections": {"Education", "Experience", "Projects", "Skills"},
    },
    {
        "name": "unusual_section_order",
        "resume": """Nora Ordered
nora@example.com
PROJECTS
Search API: Python, FastAPI, PostgreSQL
EDUCATION
M.S. Computer Science, River University
CERTIFICATIONS
PostgreSQL Associate, 2022
SKILLS
Python, FastAPI, PostgreSQL
EXPERIENCE
Engineer at Delta Tools
2022 - 2024
Built search endpoints.
""",
        "job_description": "API engineer with Python, FastAPI, PostgreSQL, and Docker.",
        "sections": {"Projects", "Education", "Certifications", "Skills", "Experience"},
    },
    {
        "name": "very_short_resume",
        "resume": """Pat Short
pat@example.com
SKILLS
Python
""",
        "job_description": "Python developer with Flask and AWS.",
        "sections": {"Skills"},
    },
    {
        "name": "long_many_sections",
        "resume": """Quinn Broad
quinn@example.com
SUMMARY
Systems developer focused on reliable automation.
SKILLS
Python, Java, JavaScript, SQL, PostgreSQL, Docker, Git, Linux
EXPERIENCE
Engineer at Atlas Systems
2018 - 2024
Maintained services and improved deployment workflows.
PROJECTS
Telemetry: Python, PostgreSQL
Built telemetry reports for 500 users.
Portal: JavaScript, React
Created an internal operations portal.
EDUCATION
M.Eng. Software Systems, Central University
CERTIFICATIONS
AWS Certified Developer, 2021
ACHIEVEMENTS
Reduced incidents by 35%.
LANGUAGES
English, Spanish
""",
        "job_description": "Systems engineer with Python, SQL, Docker, AWS, Linux, and React.",
        "sections": {"Skills", "Experience", "Projects", "Education", "Certifications"},
    },
    {
        "name": "no_job_description",
        "resume": """Robin No JD
robin@example.com
SUMMARY
Python developer.
SKILLS
Python, Flask
PROJECTS
Small API: Python, Flask
""",
        "job_description": "",
        "sections": {"Skills", "Projects"},
    },
    {
        "name": "many_matching_jd_skills",
        "resume": """Alex Match
alex@example.com
SKILLS
Python, Flask, SQL, PostgreSQL, AWS, Docker, Git, React
EXPERIENCE
Engineer at Match Labs
2020 - 2024
Built Python APIs with Flask and PostgreSQL.
PROJECTS
Deploy Hub: AWS, Docker, Git
""",
        "job_description": "Engineer with Python, Flask, SQL, PostgreSQL, AWS, Docker, Git, React, and Kubernetes.",
        "sections": {"Skills", "Experience", "Projects"},
    },
    {
        "name": "many_missing_jd_skills",
        "resume": """Devon Gaps
devon@example.com
SKILLS
HTML, CSS
EXPERIENCE
Designer at Bright Studio
2021 - 2023
Created accessible layouts.
""",
        "job_description": "Backend engineer with Python, Flask, SQL, AWS, Docker, Kubernetes, and Terraform.",
        "sections": {"Skills", "Experience"},
    },
    {
        "name": "most_jd_skills_match",
        "resume": """Chris Mostly Match
chris@example.com
SKILLS
Python, Flask, SQL, Git, Docker
PROJECTS
API Gateway: Python, Flask, SQL, Docker
""",
        "job_description": "Python Flask SQL Git Docker AWS engineer.",
        "sections": {"Skills", "Projects"},
    },
    {
        "name": "few_jd_skills_match",
        "resume": """Jamie Few Match
jamie@example.com
SKILLS
Python
PROJECTS
Script Runner: Python
""",
        "job_description": "Python, Flask, SQL, AWS, Docker, Kubernetes engineer.",
        "sections": {"Skills", "Projects"},
    },
    {
        "name": "numerical_metrics",
        "resume": """Drew Metrics
drew@example.com
EXPERIENCE
Engineer at Metric Works
2021 - 2024
Reduced latency by 45% and supported 1200 users.
PROJECTS
Batch Tool: Python
Processed 3.5 million records.
ACHIEVEMENTS
Saved $25K annually.
""",
        "job_description": "Python engineer with performance optimization experience.",
        "sections": {"Experience", "Projects"},
    },
    {
        "name": "multiple_dates",
        "resume": """Erin Timeline
erin@example.com
EXPERIENCE
Engineer at First Co
Jan 2018 - Mar 2020
Developer at Second Co
2020 - 2023
Consultant at Third Co
Apr 2023 - Present
SKILLS
Python, SQL
""",
        "job_description": "Python SQL engineer.",
        "sections": {"Experience", "Skills"},
    },
    {
        "name": "multiple_projects_technologies",
        "resume": """Frank Projects
frank@example.com
PROJECTS
Vision Tool: Python, OpenCV, TensorFlow
Commerce API: Java, Spring Boot, MySQL
Mobile Client: Kotlin, Android
SKILLS
Python, OpenCV, TensorFlow, Java, Spring Boot, MySQL, Kotlin, Android
""",
        "job_description": "Developer with Python, OpenCV, Java, MySQL, Kotlin, and AWS.",
        "sections": {"Projects", "Skills"},
    },
    {
        "name": "multiple_employers_roles",
        "resume": """Gale Roles
gale@example.com
EXPERIENCE
Lead Engineer at Oak Systems
2022 - 2025
Python platform services.
Software Engineer at Pine Systems
2019 - 2022
Java data services.
Analyst at Birch Group
2017 - 2019
SQL reporting.
SKILLS
Python, Java, SQL
""",
        "job_description": "Software engineer with Python, Java, and SQL.",
        "sections": {"Experience", "Skills"},
    },
]

SCENARIOS = {item["name"]: item for item in EDGE_CASES}
