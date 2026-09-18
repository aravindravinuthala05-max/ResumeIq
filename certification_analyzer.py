import re

def analyze_certifications(resume_text):
    """
    Detect certifications and credentials in resume.
    
    Returns:
        dict: Certification analysis with count and types
    """
    certifications = {
        "total_certifications": 0,
        "aws_certifications": [],
        "gcp_certifications": [],
        "azure_certifications": [],
        "other_certifications": [],
        "has_certifications": False
    }
    
    resume_lower = resume_text.lower()
    
    # AWS Certifications
    aws_certs = ["aws certified", "aws architect", "aws developer", "aws solutions architect"]
    for cert in aws_certs:
        if cert in resume_lower:
            certifications["aws_certifications"].append(cert)
    
    # GCP Certifications
    gcp_certs = ["gcp certified", "google cloud certified", "google associate"]
    for cert in gcp_certs:
        if cert in resume_lower:
            certifications["gcp_certifications"].append(cert)
    
    # Azure Certifications
    azure_certs = ["az-900", "az-104", "microsoft certified", "azure administrator"]
    for cert in azure_certs:
        if cert in resume_lower:
            certifications["azure_certifications"].append(cert)
    
    # Other popular certifications
    other_certs = {
        "certified": "Certified",
        "certification": "Certification",
        "scrum master": "Scrum Master",
        "pmp": "PMP",
        "cissp": "CISSP",
        "kubernetes": "Kubernetes Certification",
        "docker": "Docker Certification",
        "tensorflow": "TensorFlow Certification",
        "oracle": "Oracle Certification"
    }
    
    for keyword, cert_name in other_certs.items():
        if keyword in resume_lower and cert_name not in certifications["other_certifications"]:
            certifications["other_certifications"].append(cert_name)
    
    # Calculate total
    total = len(certifications["aws_certifications"]) + len(certifications["gcp_certifications"]) + \
            len(certifications["azure_certifications"]) + len(certifications["other_certifications"])
    
    certifications["total_certifications"] = total
    certifications["has_certifications"] = total > 0
    
    return certifications
