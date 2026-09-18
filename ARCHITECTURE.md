# ResumeIQ - System Architecture

## Overview

ResumeIQ is a modular, production-grade AI Resume Intelligence Platform built with Python and Flask. The architecture emphasizes separation of concerns, modularity, and scalability.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                              │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐  │
│  │   index.html (Upload)     │  │   result.html (Dashboard)    │  │
│  │   Modern Responsive UI    │  │   Score Breakdown & Insights │  │
│  └──────────────┬────────────┘  └──────────────┬───────────────┘  │
│                │                              │                  │
│                └──────────────┬───────────────┘                  │
│                               │                                  │
└───────────────────────────────┼──────────────────────────────────┘
                                │ (AJAX/Fetch)
                                ▼
        ┌───────────────────────────────────────────────────┐
        │          Flask REST API                            │
        │  ┌──────────────────────────────────────────────┐  │
        │  │  POST /upload                                │  │
        │  │  - Validate file & job description           │  │
        │  │  - Orchestrate analysis pipeline             │  │
        │  │  - Return comprehensive JSON                 │  │
        │  └──────────────────────────────────────────────┘  │
        └──────────────────┬─────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────────────────────┐
        │   ANALYSIS PIPELINE                               │
        │                                                     │
        │  ┌─────────────────────────────────────────────┐  │
        │  │ 1. Resume Parser (resume_parser.py)          │  │
        │  │    - PDF text extraction                      │  │
        │  │    - Raw text preprocessing                   │  │
        │  └─────────────────┬───────────────────────────┘  │
        │                    │                               │
        │  ┌─────────────────▼───────────────────────────┐  │
        │  │ 2. Parallel Analyzers (10 Independent)      │  │
        │  │                                               │  │
        │  │    ├─ contact_analyzer.py                    │  │
        │  │    │   → {email, phone, linkedin, github}    │  │
        │  │    │                                          │  │
        │  │    ├─ section_detector.py                    │  │
        │  │    │   → {education, experience, ...}        │  │
        │  │    │                                          │  │
        │  │    ├─ education_analyzer.py                  │  │
        │  │    │   → {degree, college, branch, cgpa}     │  │
        │  │    │                                          │  │
        │  │    ├─ experience_analyzer.py                 │  │
        │  │    │   → {internships, companies, roles}     │  │
        │  │    │                                          │  │
        │  │    ├─ project_analyzer.py                    │  │
        │  │    │   → {total, ai, web, mobile, iot}       │  │
        │  │    │                                          │  │
        │  │    ├─ certification_analyzer.py              │  │
        │  │    │   → {aws, gcp, azure, others}           │  │
        │  │    │                                          │  │
        │  │    ├─ achievement_analyzer.py                │  │
        │  │    │   → {metrics, impact_keywords}          │  │
        │  │    │                                          │  │
        │  │    ├─ language_analyzer.py                   │  │
        │  │    │   → {programming, scripting, natural}   │  │
        │  │    │                                          │  │
        │  │    └─ formatting_analyzer.py                 │  │
        │  │        → {score, issues, strengths}          │  │
        │  │                                               │  │
        │  └─────────────────┬───────────────────────────┘  │
        │                    │                               │
        │  ┌─────────────────▼───────────────────────────┐  │
        │  │ 3. Skill Matching (ats_engine.py)           │  │
        │  │    - Extract skills from resume              │  │
        │  │    - Extract skills from job description     │  │
        │  │    - Calculate basic matching score           │  │
        │  │    → {matched_skills, missing_skills}        │  │
        │  └─────────────────┬───────────────────────────┘  │
        │                    │                               │
        │  ┌─────────────────▼───────────────────────────┐  │
        │  │ 4. Weighted Scoring (score_engine.py)       │  │
        │  │    - Skills: 40%                              │  │
        │  │    - Projects: 20%                            │  │
        │  │    - Experience: 15%                          │  │
        │  │    - Education: 10%                           │  │
        │  │    - Sections: 10%                            │  │
        │  │    - Formatting: 5%                           │  │
        │  │    → {overall_score, breakdown, status}       │  │
        │  └─────────────────┬───────────────────────────┘  │
        │                    │                               │
        │  ┌─────────────────▼───────────────────────────┐  │
        │  │ 5. Recommendations (resume_advisor.py)      │  │
        │  │    - Intelligent suggestions                 │  │
        │  │    - Skill-specific advice                   │  │
        │  │    - Formatting improvements                 │  │
        │  │    → {[recommendations]}                      │  │
        │  └─────────────────┬───────────────────────────┘  │
        │                    │                               │
        │  ┌─────────────────▼───────────────────────────┐  │
        │  │ 6. Interview Questions (interview_gen.py)   │  │
        │  │    - Generate from projects                  │  │
        │  │    - Generate from skills                    │  │
        │  │    - Generate from experience                │  │
        │  │    - Generate from education                 │  │
        │  │    - Generate role-specific questions        │  │
        │  │    → {[questions]}                            │  │
        │  └─────────────────┬───────────────────────────┘  │
        │                    │                               │
        └────────────────────┼───────────────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │  Aggregated      │
                    │  Analysis Result │
                    │  (JSON)          │
                    └────────┬─────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
        ┌────────────┐ ┌──────────┐ ┌──────────────┐
        │ Frontend   │ │ Terminal │ │ Session      │
        │ Display    │ │ Logging  │ │ Storage      │
        │ (result.js)│ │ (app.py) │ │ (JS)         │
        └────────────┘ └──────────┘ └──────────────┘
```

## Component Details

### 1. Frontend Layer

#### index.html
- Modern, responsive upload interface
- Drag-and-drop file upload
- Real-time file validation
- Job description textarea

#### result.html
- Comprehensive dashboard
- Score visualization (circular progress)
- Score breakdown by category
- Skills display
- Recommendations list
- Interview questions
- Formatting analysis

#### CSS (style.css)
- Mobile-first responsive design
- Modern gradient styling
- Smooth animations
- Accessibility considerations

#### JavaScript (script.js & result.js)
- Form submission handling
- AJAX file upload
- Client-side validation
- Result visualization
- Data persistence (sessionStorage)

### 2. Backend Layer (Flask)

#### app.py (Main Application)
```python
Routes:
  GET  / → Home page
  POST /upload → Analyze resume (API)
  GET  /result → Results page
  GET  /health → Health check
```

**Key Functions:**
- Request validation
- Orchestrate analyzer pipeline
- Error handling
- Response formatting
- Console logging for debugging

#### Resume Parser (resume_parser.py)
- Extract text from PDF files
- Handle multi-page PDFs
- Clean and normalize text

### 3. Analysis Engine (10 Independent Modules)

Each analyzer is a standalone Python module following this pattern:

```python
def analyze_X(resume_text):
    """
    Analyze specific aspect of resume.
    
    Returns:
        dict: Structured analysis results
    """
    analysis = {}
    # ... analysis logic ...
    return analysis
```

**Analyzers:**

1. **contact_analyzer.py** - Extract contact information
   - Email regex pattern matching
   - Phone number extraction
   - LinkedIn/GitHub profile detection
   - Personal website identification

2. **section_detector.py** - Detect resume sections
   - Keyword-based section detection
   - Presence/absence boolean flags
   - Multiple section support

3. **education_analyzer.py** - Extract education details
   - Degree classification (B.Tech, B.Sc, M.Tech, etc.)
   - Branch/specialization detection
   - College/university extraction
   - CGPA/marks extraction
   - Graduation year detection

4. **experience_analyzer.py** - Extract experience information
   - Internship counting
   - Company name detection
   - Role/position identification
   - Experience duration calculation

5. **project_analyzer.py** - Categorize projects
   - Total project count
   - AI/ML project detection
   - Web project detection
   - Mobile project detection
   - IoT project detection

6. **certification_analyzer.py** - Extract certifications
   - AWS certifications
   - GCP certifications
   - Azure certifications
   - Other relevant certifications
   - Certification aggregation

7. **achievement_analyzer.py** - Extract quantified achievements
   - Action verb counting
   - Metric extraction (percentages, money, time)
   - Impact keyword identification
   - Achievement scoring

8. **language_analyzer.py** - Detect programming languages
   - Programming languages (Python, Java, C++, etc.)
   - Scripting languages (Bash, PowerShell, etc.)
   - Markup languages (HTML, XML, JSON, etc.)
   - Natural languages (English, Spanish, etc.)

9. **formatting_analyzer.py** - Analyze formatting quality
   - Resume length validation
   - Bullet point usage
   - Date format consistency
   - Special character detection
   - Table usage detection
   - ATS compatibility scoring

10. **skill.py** - Skill definitions
    - PROGRAMMING_LANGUAGES list
    - FRAMEWORKS list
    - DATABASES list
    - CLOUD list
    - AI_ML list
    - DEVOPS list

### 4. Scoring Engine (score_engine.py)

**Weighted Scoring Algorithm:**

```
Overall Score = 
    (Skills Score × 40/100) +
    (Projects Score × 20/100) +
    (Experience Score × 15/100) +
    (Education Score × 10/100) +
    (Sections Score × 10/100) +
    (Formatting Score × 5/100)
```

**Details:**

- **Skills Score (40%)**
  - Based on matched skills percentage
  - 80%+ match = Full credit
  - Scaled down for lower percentages

- **Projects Score (20%)**
  - 5 points for having projects section
  - +3 points for each project type (AI, Web, Mobile, IoT)
  - +3 points for 5+ total projects
  - +2 points for 3-4 projects
  - +1 point for 1-2 projects

- **Experience Score (15%)**
  - 5 points base
  - +2 per internship (max 5)
  - +3 for having companies
  - +2 for multiple companies
  - +2 for having roles

- **Education Score (10%)**
  - 4 points base
  - +2 for having degree
  - +2 for having college
  - +2 for having CGPA

- **Sections Score (10%)**
  - 2 points per detected section
  - 5 sections max = 10 points

- **Formatting Score (5%)**
  - Base score from formatting_analyzer
  - Scaled to 0-5 range

### 5. Recommendation Engine (resume_advisor.py)

**Intelligent Recommendations:**

- Skill-specific advice (50+ skills covered)
- Achievement enhancement suggestions
- Formatting improvement recommendations
- Missing section identification
- ATS optimization tips
- Generic best-practice recommendations
- Duplicate removal while preserving priority

### 6. Interview Question Generator (interview_generator.py)

**Question Generation Strategy:**

1. **Project-based questions** (if projects found)
2. **Skill-based questions** (top 5 skills)
3. **Experience-based questions** (if experience found)
4. **Education-based questions** (if education found)
5. **Technical depth questions** (always included)
6. **Soft skills questions** (always included)
7. **Role-specific questions** (based on job description)

## Data Flow

### Input
```json
{
  "resume": "PDF file",
  "job_description": "string"
}
```

### Processing
1. Parse resume PDF
2. Run 10 analyzers in parallel
3. Calculate basic skill match
4. Calculate weighted overall score
5. Generate recommendations
6. Generate interview questions
7. Compile comprehensive report

### Output
```json
{
  "success": true,
  "resume_name": "string",
  "analysis_timestamp": "ISO 8601",
  
  "contact": { /* contact info */ },
  "education": { /* education info */ },
  "experience": { /* experience info */ },
  "projects": { /* projects info */ },
  "certifications": { /* certs info */ },
  "achievements": { /* achievements */ },
  "languages": { /* languages */ },
  "formatting": { /* formatting */ },
  "sections": { /* sections */ },
  
  "overall_ats_score": 78.5,
  "status": "✅ Good Match",
  "score_breakdown": { /* breakdown */ },
  "matched_skills": [/* list */],
  "missing_skills": [/* list */],
  
  "suggestions": [/* recommendations */],
  "interview_questions": [/* questions */]
}
```

## Design Patterns

### 1. Modular Architecture
- Each analyzer is independent
- Can be used standalone or together
- Easy to test and maintain
- Easy to extend with new analyzers

### 2. Separation of Concerns
- Parser handles PDF extraction
- Analyzers handle specific aspects
- Scoring engine handles calculation
- Recommendation engine handles suggestions
- Frontend handles display

### 3. Dictionary-based Communication
- All components return dictionaries
- Consistent interface
- Easy to serialize to JSON
- Easy to log and debug

### 4. Declarative Configuration
- Skill lists defined in one place (skill.py)
- Keyword lists defined in analyzers
- Easy to update and maintain

## Error Handling

```
PDF Upload
  ├─ File validation
  │  ├─ File size check
  │  ├─ File type check
  │  └─ File readability check
  │
  ├─ Text extraction
  │  ├─ PDF parsing error handling
  │  └─ Empty text handling
  │
  └─ Analysis
     ├─ Missing data handling
     └─ Invalid data handling
```

## Performance Considerations

### Current
- Sequential processing
- Suitable for small datasets
- Fast enough for individual use

### Scalability Opportunities
1. **Parallel Processing**: Run analyzers in parallel threads
2. **Caching**: Cache skill lists and common patterns
3. **Async**: Use async/await for I/O operations
4. **Database**: Store analyses for historical data
5. **API Optimization**: Add pagination, filtering
6. **Frontend**: Add lazy loading for results

## Security

### Current Implementation
- File type validation
- File size limit (16MB)
- No sensitive data storage

### Production Recommendations
1. **Authentication**: User login system
2. **Authorization**: Role-based access
3. **Encryption**: HTTPS, data encryption
4. **Input Validation**: Comprehensive input checks
5. **CSRF Protection**: CSRF tokens
6. **SQL Injection**: Use ORM (if database added)
7. **XSS Prevention**: Template escaping
8. **Rate Limiting**: API rate limits
9. **Logging**: Audit logs
10. **Data Retention**: Automatic cleanup

## Deployment Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create `.env` file from `.env.example`
- [ ] Test: `python -m py_compile *.py`
- [ ] Run: `python app.py`
- [ ] Test upload: Upload test resume and job description
- [ ] Verify output: Check score, recommendations, questions
- [ ] Setup logging: Configure application logging
- [ ] Setup monitoring: Add health checks
- [ ] Setup backups: Configure file backups
- [ ] Setup CDN: Serve static files from CDN

## Future Architecture Enhancements

### Phase 1
- User authentication system
- Database integration
- Resume storage
- Analysis history
- API documentation

### Phase 2
- Async task processing
- Caching layer (Redis)
- Machine learning models
- Advanced analytics

### Phase 3
- Microservices architecture
- Event-driven processing
- Real-time updates
- Global deployment

---

**Built for Production. Built for Scale. Built for Success.** 🚀
