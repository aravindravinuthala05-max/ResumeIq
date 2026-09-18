import re

def analyze_contact(resume_text):
    """
    Extract and analyze contact information from resume.
    
    Returns:
        dict: Contact information including email, phone, LinkedIn, GitHub
    """
    contact_info = {
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "website": None,
        "location": None
    }
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, resume_text)
    if emails:
        contact_info["email"] = emails[0]
    
    # Phone pattern
    phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, resume_text)
    if phones:
        contact_info["phone"] = phones[0]
    
    # LinkedIn
    if "linkedin" in resume_text.lower():
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', resume_text.lower())
        if linkedin_match:
            contact_info["linkedin"] = linkedin_match.group(0)
        else:
            contact_info["linkedin"] = "linkedin.com profile mentioned"
    
    # GitHub
    if "github" in resume_text.lower():
        github_match = re.search(r'github\.com/[\w-]+', resume_text.lower())
        if github_match:
            contact_info["github"] = github_match.group(0)
        else:
            contact_info["github"] = "github.com profile mentioned"
    
    # Website/Portfolio
    website_pattern = r'https?://(?:www\.)?[\w.-]+\.\w+'
    websites = re.findall(website_pattern, resume_text)
    if websites:
        contact_info["website"] = websites[0]
    
    return contact_info
