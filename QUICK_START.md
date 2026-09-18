# ResumeIQ - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

You'll see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 3: Open in Browser
Visit: **http://localhost:5000**

### Step 4: Test the Application

1. **Upload a Resume**
   - Click "Drag & Drop Your Resume" or browse to select a PDF
   - Or drag and drop a PDF file

2. **Paste Job Description**
   - Copy and paste a job description from any job portal
   - Include required skills, responsibilities, qualifications

3. **Click "Analyze Resume"**
   - Wait for analysis to complete (usually 2-5 seconds)
   - You'll see a comprehensive dashboard

4. **Review Results**
   - 📊 ATS Score (0-100)
   - ✅ Matched Skills
   - ❌ Missing Skills
   - 💡 Recommendations
   - ❓ Interview Questions
   - 📐 Formatting Analysis

## 📋 Sample Test Data

### Sample Resume Text (for testing without PDF)
```
John Doe
john@example.com | (555) 123-4567
LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe

EDUCATION
B.Tech in Computer Science
Indian Institute of Technology Delhi
Graduation: May 2023
CGPA: 8.5/10

EXPERIENCE
Software Engineer Intern
TCS (Tata Consultancy Services)
Jun 2022 - Aug 2022
- Developed REST APIs using Flask
- Optimized database queries, reducing load by 30%
- Worked with Python and SQL

PROJECTS
1. ResumeIQ - AI Resume Intelligence Platform
   - Flask backend with 10 AI analyzers
   - Modern responsive frontend
   - Weighted ATS scoring algorithm

2. E-commerce Website
   - React frontend, Django backend
   - Payment integration using Stripe
   - 50% improvement in page load time

SKILLS
Programming Languages: Python, Java, JavaScript
Frameworks: Flask, Django, React
Databases: SQL, PostgreSQL, MongoDB
Cloud: AWS, Google Cloud
DevOps: Git, Docker, GitHub Actions
AI/ML: TensorFlow, Scikit-learn, Pandas

CERTIFICATIONS
- AWS Solutions Architect Associate
- Google Cloud Associate Cloud Engineer
```

### Sample Job Description
```
Senior Software Engineer (Python/Flask)

Company: Tech Startup XYZ

We're looking for an experienced Senior Software Engineer to lead our backend team.

Required Skills:
- 5+ years Python experience
- Strong Flask/FastAPI background
- Proficiency in SQL and PostgreSQL
- AWS or GCP experience
- Docker and Kubernetes knowledge
- Git and CI/CD experience
- Strong problem-solving skills

Responsibilities:
- Design and implement scalable APIs
- Mentor junior developers
- Optimize database performance
- Implement security best practices
- Participate in code reviews

Preferred:
- Machine Learning experience
- DevOps background
- Open source contributions
- Experience with microservices
```

## 📊 Expected Output

### Console Output
```
============================================================
RESUMEIQ ANALYSIS REPORT
============================================================
Resume: sample_resume.pdf
Timestamp: 2024-01-15 10:30:45
------------------------------------------------------------

📋 CONTACT INFORMATION:
  Email: john@example.com
  Phone: (555) 123-4567
  LinkedIn: linkedin.com/in/johndoe
  GitHub: github.com/johndoe

🎓 EDUCATION:
  Degree: B.TECH
  College: Indian Institute of Technology Delhi
  Branch: COMPUTER SCIENCE
  CGPA: 8.5

💼 EXPERIENCE:
  Found: True
  Internships: 1
  Companies: TCS
  Roles: Software Engineer

🚀 PROJECTS:
  Total: 2
  AI Projects: 1
  Web Projects: 1
  Mobile Projects: 0

📜 CERTIFICATIONS:
  Total: 2

⭐ ACHIEVEMENTS:
  Total Actions: 5
  Quantified: 3
  Achievement Score: 72/100

💬 LANGUAGES:
  Programming: 3
  Natural: 1

📐 FORMATTING:
  Score: 78/100
  ATS Compatible: True

📊 RESUME SECTIONS DETECTED:
  ✅ Education
  ✅ Experience
  ✅ Projects
  ✅ Skills
  ✅ Certifications

🎯 ATS SCORE BREAKDOWN:
  Skills: 32/40
  Projects: 18/20
  Experience: 13/15
  Education: 9/10
  Sections: 8/10
  Formatting: 4.5/5
  ───────────────────────────
  OVERALL: 84.5/100
  STATUS: ✅ Good Match
```

### Web Dashboard
- Circular ATS score display
- Score breakdown with progress bars
- Matched/missing skills with badges
- Contact information cards
- Education, experience, projects details
- Certifications list
- Languages detected
- 10+ personalized recommendations
- 15+ interview questions
- Formatting analysis with strengths/issues
- Download report button
- Analyze another resume button

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution:**
```bash
python app.py --port 5001
```

### Issue: "PDF file not supported"
**Solution:**
- Ensure file is a valid PDF
- Check file is not corrupted
- Try with a different PDF file

### Issue: "No analysis results displayed"
**Solution:**
- Check browser console for errors (F12)
- Verify job description is not empty
- Try with a simpler resume file

### Issue: "Application won't start"
**Solution:**
```bash
# Check Python version (should be 3.8+)
python --version

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run with verbose output
python -u app.py
```

## 📚 Module Testing

### Test Individual Analyzers
```python
from contact_analyzer import analyze_contact
resume = "email: john@example.com, phone: (555) 123-4567"
print(analyze_contact(resume))

from education_analyzer import analyze_education
resume = "B.Tech from IIT Delhi, CGPA 8.5"
print(analyze_education(resume))

from skill import PROGRAMMING_LANGUAGES
print(PROGRAMMING_LANGUAGES)
```

### Test Full Pipeline
```bash
python -c "
from resume_parser import extract_text
from ats_engine import calculate_ats_score
from score_engine import calculate_weighted_ats_score

resume = extract_text('path/to/resume.pdf')
result = calculate_ats_score(resume, 'job description')
print(result)
"
```

## 🎯 Next Steps

### For Development
1. Read ARCHITECTURE.md for system design
2. Check individual analyzer modules
3. Explore score_engine.py for scoring logic
4. Customize recommendation engine

### For Deployment
1. Create .env file with production settings
2. Install database (PostgreSQL recommended)
3. Add user authentication
4. Setup HTTPS/SSL
5. Deploy to cloud (AWS, GCP, Heroku)

### For Enhancement
1. Add more skill definitions to skill.py
2. Create new analyzers for additional features
3. Improve ML models for scoring
4. Add more recommendation rules
5. Integrate with job portals API

## 💡 Tips

1. **Better Results**: Use complete, well-formatted resumes
2. **Accuracy**: Paste full job descriptions
3. **Recommendations**: Follow the top 5 suggestions
4. **Interview Prep**: Practice answers to generated questions
5. **Iteration**: Use tool multiple times to improve scores

## 📞 Support

### Common Questions

**Q: How accurate is the ATS score?**
A: The score is based on comprehensive analysis of 100+ resume aspects. It's a good indicator but not 100% accurate to actual ATS systems.

**Q: Can I analyze multiple resumes?**
A: Yes! Each analysis is independent. Use "Analyze Another Resume" to start fresh.

**Q: Is my data stored anywhere?**
A: No, current version doesn't store data. It's analyzed and displayed immediately.

**Q: Can I export the results?**
A: Yes, download PDF report feature is available (coming soon in enhanced version).

**Q: Works on mobile?**
A: Yes, the interface is fully responsive and works on mobile browsers.

## 🚀 Ready to Improve Your Resume?

1. **Upload** your resume
2. **Paste** a job description
3. **Analyze** and get insights
4. **Improve** based on recommendations
5. **Repeat** until you get to 90+!

---

**Happy Resume Building! Get Hired Faster with ResumeIQ!** 🎯
