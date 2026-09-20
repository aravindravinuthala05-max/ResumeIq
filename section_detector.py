from resume_sections import clean_lines, section_for_heading


def detect_resume_sections(resume_text):
    """Detect actual heading lines, never incidental words in resume prose."""
    found = {section_for_heading(line) for line in clean_lines(resume_text)}
    return {
        "Education": "education" in found,
        "Experience": "experience" in found,
        "Projects": "projects" in found,
        "Skills": "skills" in found,
        "Certifications": "certifications" in found,
    }
