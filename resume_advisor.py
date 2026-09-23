"""
Resume Advisor - Intelligent Recommendation Engine

Generates actionable recommendations based on:
- Missing skills
- Weak areas in resume
- Formatting issues
- Achievement metrics
"""

def generate_suggestions(
    missing_skills,
    formatting_issues=None,
    achievements_info=None,
    sections_present=None,
    matched_skills=None,
    score_breakdown=None
):
    """
    Generate intelligent, actionable recommendations.
    
    Args:
        missing_skills: list of skills not in resume
        formatting_issues: list of formatting issues
        achievements_info: dict from achievement_analyzer
        sections_present: dict of resume sections
        matched_skills: list of matched skills
        score_breakdown: dict from score_engine
    
    Returns:
        list: Prioritized recommendations
    """
    # Legacy callers still receive useful guidance, but it must obey the same
    # evidence rules as the structured advisor below.  In particular, never
    # turn a JD keyword into a claim that the candidate has used it.
    missing_skills = missing_skills if isinstance(missing_skills, list) else []
    matched_skills = matched_skills if isinstance(matched_skills, list) else []
    formatting_issues = formatting_issues if isinstance(formatting_issues, list) else []
    sections_present = sections_present if isinstance(sections_present, dict) else {}
    suggestions = [
        f"{skill} is not evidenced in your resume. Learn the fundamentals and add it only after gaining genuine, supportable experience."
        for skill in missing_skills
    ]
    if achievements_info and achievements_info.get("quantified_achievements", 0) == 0:
        suggestions.append("Add a measurable result only if you can verify it from your actual work; do not estimate or invent one.")
    if formatting_issues:
        suggestions.append(f"Formatting: {formatting_issues[0]}")
    if sections_present and not sections_present.get("Summary", False):
        suggestions.append("Add a concise summary using only your verified background and target-role alignment.")
    if matched_skills:
        suggestions.append("Keep matched skills connected to the project or experience where you actually used them.")
    return suggestions or ["No additional action is required based on the available resume evidence."]

    # Retained below only as historical reference for a future legacy API
    # migration; execution intentionally ends at the evidence-grounded return.
    
    suggestions = []
    
    # ==================== SKILL-BASED RECOMMENDATIONS ====================
    skill_advice = {
        "python": "Add Python projects to demonstrate proficiency. Include GitHub links.",
        "sql": "Add real-world SQL query examples or database design projects.",
        "flask": "Build and showcase a Flask web application with deployment details.",
        "fastapi": "Create a FastAPI project with proper API documentation (Swagger).",
        "git": "Include your GitHub profile link and showcase open-source contributions.",
        "github": "Create a GitHub profile and link 3-5 of your best projects.",
        "docker": "Containerize one of your projects using Docker and mention in resume.",
        "aws": "Deploy a project on AWS (EC2, Lambda, S3) and document the process.",
        "gcp": "Add experience deploying to Google Cloud Platform.",
        "kubernetes": "Include Kubernetes orchestration experience if available.",
        "machine learning": "Add ML projects with datasets, models, and evaluation metrics.",
        "tensorflow": "Build TensorFlow projects with clear model architecture and results.",
        "pytorch": "Showcase PyTorch projects with training metrics and model performance.",
        "react": "Build and deploy a React application with modern state management.",
        "angular": "Create an Angular application showing component architecture.",
        "nodejs": "Add Node.js backend projects with proper API design.",
        "mongodb": "Include NoSQL database projects showing schema design.",
        "postgresql": "Add SQL database projects showing optimization and indexing.",
        "rest api": "Design and document comprehensive REST APIs.",
        "microservices": "Add projects using microservices architecture.",
        "ci/cd": "Implement CI/CD pipelines using GitHub Actions or Jenkins.",
        "devops": "Showcase infrastructure automation and deployment expertise.",
        "cloud": "Add cloud deployment experience (AWS, GCP, Azure).",
        "agile": "Mention Scrum/Agile experience with specific tools used."
    }
    
    # High-priority missing skills
    for skill in missing_skills[:8]:
        skill_lower = skill.lower()
        if skill_lower in skill_advice:
            suggestions.append(f"🎯 {skill_advice[skill_lower]}")
    
    # ==================== ACHIEVEMENT RECOMMENDATIONS ====================
    if achievements_info:
        if achievements_info.get("quantified_achievements", 0) == 0:
            suggestions.append("📊 Add quantifiable metrics to your achievements (e.g., '30% faster', '$50K saved').")
        
        if achievements_info.get("achievement_score", 0) < 50:
            suggestions.append("⭐ Highlight your impact: Use action verbs and measurable results.")
    
    # ==================== FORMATTING RECOMMENDATIONS ====================
    if formatting_issues:
        if len(formatting_issues) > 0:
            suggestions.append(f"📝 Formatting: {formatting_issues[0]}")
    
    # ==================== SECTION RECOMMENDATIONS ====================
    if sections_present:
        missing_sections = []
        if not sections_present.get("Summary", False):
            missing_sections.append("Professional Summary")
        if not sections_present.get("Contact", False):
            missing_sections.append("Contact Information")
        if not sections_present.get("Certifications", False):
            missing_sections.append("Certifications")
        
        if missing_sections:
            suggestions.append(f"📋 Add missing sections: {', '.join(missing_sections)}")
    
    # ==================== CONTENT RECOMMENDATIONS ====================
    if matched_skills and len(matched_skills) > 0:
        suggestions.append(f"✅ Leverage your {len(matched_skills)} matched skills in your cover letter.")
    
    suggestions.extend([
        "🔗 Add links to your GitHub, LinkedIn, and portfolio.",
        "📱 Include a professional summary at the top of your resume.",
        "🎯 Tailor your resume for each job application.",
        "✨ Use bullet points for better readability and ATS compatibility.",
        "⚡ Keep your resume to 1 page if you have <5 years of experience."
    ])
    
    # Remove duplicates while preserving order
    unique_suggestions = []
    seen = set()
    for suggestion in suggestions:
        if suggestion not in seen:
            seen.add(suggestion)
            unique_suggestions.append(suggestion)
    
    if not unique_suggestions:
        unique_suggestions.append(
            "✨ Excellent! Your resume is well-structured. Minor tweaks: ensure all links are working and update dates."
        )
    
    return unique_suggestions


# Legacy function for backward compatibility
def generate_suggestions_legacy(missing_skills):
    return generate_suggestions(missing_skills)


def _recommendation(title, description, priority, section, source, evidence=None, jd_relevance=False):
    return {
        "title": title,
        "description": description,
        "priority": priority,
        "section": section,
        "source": source,
        "evidence": list(evidence or []),
        "jd_relevance": bool(jd_relevance),
        "fact_safe": True,
    }


def _evidence_values(evidence, section):
    return [item for item in (evidence or {}).get(section, []) if isinstance(item, dict) and item.get("value")]


def generate_advice(
    missing_skills=None,
    formatting_issues=None,
    achievements_info=None,
    sections_present=None,
    matched_skills=None,
    score_breakdown=None,
    resume_evidence=None,
    job_description="",
):
    """Return deterministic structured advice alongside legacy suggestions."""
    missing_skills = missing_skills if isinstance(missing_skills, list) else []
    matched_skills = matched_skills if isinstance(matched_skills, list) else []
    formatting_issues = formatting_issues if isinstance(formatting_issues, list) else []
    sections_present = sections_present if isinstance(sections_present, dict) else {}
    evidence = resume_evidence if isinstance(resume_evidence, dict) else {}
    jd_text = job_description if isinstance(job_description, str) else ""
    recommendations = []

    for skill in matched_skills:
        clean_skill = str(skill).split(" (", 1)[0]
        supported = [item for item in _evidence_values(evidence, "technologies") if str(item.get("value", "")).casefold() == clean_skill.casefold()]
        if supported:
            recommendations.append(_recommendation(
                f"Emphasize {clean_skill} for this role",
                f"{clean_skill} is supported by your resume evidence and matches the target job description. Keep it visible in the relevant skills or project context.",
                "LOW", "Skills", "resume_evidence", [clean_skill], True,
            ))

    for skill in missing_skills:
        skill_text = str(skill).split(" (", 1)[0]
        recommendations.append(_recommendation(
            f"Review the {skill_text} requirement",
            f"{skill_text} appears in the target job description but is not supported by the current resume evidence. Add it only if you genuinely have verified experience with {skill_text}.",
            "HIGH", "Skills", "job_description", [skill_text], True,
        ))

    projects = _evidence_values(evidence, "projects")
    project_details = [item for item in projects if item.get("type") == "project_detail" and len(str(item.get("value", "")).split()) >= 4]
    project_names = [item for item in projects if item.get("type") == "project"]
    if project_names and not project_details:
        recommendations.append(_recommendation(
            "Expand project descriptions",
            "Your resume names a project but does not provide enough verified implementation detail. Add the actual approach, tools, or outcome you can support from your experience.",
            "HIGH", "Projects", "resume_evidence", [item["value"] for item in project_names[:3]], False,
        ))

    experience = _evidence_values(evidence, "experience")
    if experience and not any(item.get("type") == "experience_detail" for item in experience):
        recommendations.append(_recommendation(
            "Clarify experience contributions",
            "Your experience section identifies roles or employers but has limited responsibility detail. Add only responsibilities and outcomes that are directly supported by your work.",
            "MEDIUM", "Experience", "resume_evidence", [item["value"] for item in experience[:3]], False,
        ))

    if achievements_info and achievements_info.get("quantified_achievements", 0) == 0:
        recommendations.append(_recommendation(
            "Strengthen achievement evidence",
            "Add a metric if you have a verified one; do not estimate or invent a result.",
            "MEDIUM", "Achievements", "achievement_analyzer", [], False,
        ))

    for issue in formatting_issues[:1]:
        recommendations.append(_recommendation("Address resume formatting", str(issue), "MEDIUM", "Formatting", "formatting_analyzer", [str(issue)], False))

    if not sections_present.get("Summary", False):
        recommendations.append(_recommendation(
            "Add a concise summary",
            "Add a short summary using only your verified background, skills, and target-role alignment.",
            "MEDIUM", "Summary", "section_detector", [], False,
        ))

    if jd_text and not missing_skills and matched_skills:
        recommendations.append(_recommendation(
            "Preserve the strongest role matches",
            "Your current resume evidence supports multiple job-description skills. Keep those technologies connected to the projects or experience where they are actually used.",
            "LOW", "Skills", "resume_evidence", [str(skill).split(" (", 1)[0] for skill in matched_skills[:5]], True,
        ))

    seen = set()
    unique = []
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    for item in sorted(recommendations, key=lambda value: priority_order.get(value["priority"], 9)):
        key = (item["title"].casefold(), item["section"].casefold())
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return {
        "recommendations": unique,
        "suggestions": generate_suggestions(missing_skills, formatting_issues, achievements_info, sections_present, matched_skills, score_breakdown),
    }
