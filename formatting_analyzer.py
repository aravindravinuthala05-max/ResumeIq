def analyze_formatting(resume_text):
    """
    Analyze resume formatting quality and ATS compatibility.
    
    Returns:
        dict: Formatting analysis with score and recommendations
    """
    formatting = {
        "formatting_score": 0,
        "issues": [],
        "strengths": [],
        "ats_compatible": True
    }
    
    lines = resume_text.split('\n')
    words = resume_text.split()
    
    # Check for reasonable length
    if 300 < len(words) < 1500:
        formatting["strengths"].append("Resume length is optimal (300-1500 words)")
    elif len(words) < 300:
        formatting["issues"].append("Resume is too short. Aim for 300-1500 words")
    else:
        formatting["issues"].append("Resume is too long. Keep it under 1500 words")
    
    # Check for bullet points (good formatting indicator)
    bullet_count = sum(1 for line in lines if line.strip().startswith(('•', '-', '*', '◦')))
    if bullet_count > 5:
        formatting["strengths"].append("Good use of bullet points for readability")
    else:
        formatting["issues"].append("Add more bullet points for better readability")
    
    # Check for consistent formatting
    email_present = "@" in resume_text
    phone_present = any(char.isdigit() for char in resume_text)
    
    if email_present:
        formatting["strengths"].append("Email address is included")
    else:
        formatting["issues"].append("Email address is missing")
    
    if phone_present:
        formatting["strengths"].append("Phone number is included")
    else:
        formatting["issues"].append("Phone number is missing")
    
    # Check for special characters that might cause ATS issues
    problematic_chars = ['™', '®', '©', '†', '‡']
    for char in problematic_chars:
        if char in resume_text:
            formatting["issues"].append(f"Remove special character '{char}' for ATS compatibility")
            formatting["ats_compatible"] = False
    
    # Check for tables (generally not ATS-friendly)
    if '┌' in resume_text or '├' in resume_text or '│' in resume_text:
        formatting["issues"].append("Avoid tables; use simple text formatting instead")
        formatting["ats_compatible"] = False
    
    # Check for consistent date formats
    date_indicators = resume_text.count('20') + resume_text.lower().count('jan') + \
                     resume_text.lower().count('feb') + resume_text.lower().count('mar')
    if date_indicators > 3:
        formatting["strengths"].append("Dates are properly included")
    
    # Calculate formatting score
    score = 50  # Base score
    score += len(formatting["strengths"]) * 10
    score -= len(formatting["issues"]) * 5
    formatting["formatting_score"] = min(100, max(0, score))
    
    return formatting
