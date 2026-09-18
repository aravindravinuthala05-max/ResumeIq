# ResumeIQ

## AI Resume Intelligence Platform

**Analyze - Improve - Get Hired**

ResumeIQ is a deterministic, rule-based resume intelligence platform. It extracts resume text, analyzes resume sections, compares supported skills with a target job description, produces evidence-backed recommendations, previews factual rewrites, prepares interview questions, and generates a PDF report.

The project follows this workflow:

**ANALYZE -> UNDERSTAND -> IMPROVE -> PREPARE -> GET HIRED**

ResumeIQ does not call ChatGPT, OpenAI, Gemini, Claude, or another external AI/LLM provider.

## Project Overview

ResumeIQ helps a candidate understand how well a resume aligns with a specific role. The system keeps analysis explainable by using deterministic parsing, keyword matching, analyzer modules, structured evidence, and rule-based recommendations.

## Problem Statement

Resume review is often slow and difficult to verify. Candidates need to know which resume facts are relevant to a job, which requirements are not supported, what should be improved first, and how to prepare for likely interview topics without inventing experience.

## Objectives

- Extract useful information from PDF and DOCX resumes.
- Calculate a consistent ATS-oriented score.
- Compare resume-supported skills with a job description.
- Preserve traceable evidence and factual boundaries.
- Provide prioritized, actionable improvements.
- Offer safe rewrite previews and grounded interview questions.
- Present results in one dashboard and downloadable PDF report.

## Key Features

- PDF and DOCX text extraction.
- Contact, education, experience, project, certification, achievement, language, and formatting analysis.
- Weighted ATS score and category breakdown.
- JD-matched and missing skill lists.
- Resume, matched, missing, and evidence-backed Skills Intelligence.
- Evidence-backed Resume Advisor recommendations with HIGH, MEDIUM, and LOW priority.
- Rule-based, fact-preserving Resume Rewriter.
- Resume-grounded Interview Preparation with JD-gap questions.
- Resume Health Summary.
- Responsive continuous dashboard with secondary Resume Details.
- Backend-generated PDF report.
- Empty and malformed-input handling.

## System Architecture

The Flask application receives an upload, extracts text, runs independent analyzers, builds structured resume evidence, calculates ATS results, generates advisor and interview data, and returns one JSON-safe analysis payload. The browser stores that payload in session storage for the result dashboard. Rewriter suggestions are loaded lazily through `/rewrite`; PDF generation uses `/generate_pdf`.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the complete flow.

## Technology Stack

- Python 3.8+
- Flask
- PyPDF2 for PDF extraction
- Python standard library ZIP/XML handling for DOCX extraction
- ReportLab for PDF report generation
- HTML, CSS, and vanilla JavaScript
- pytest for automated testing

## Project Structure

```text
ResumeIQ/
├── app.py
├── resume_parser.py
├── ats_engine.py
├── score_engine.py
├── resume_evidence.py
├── resume_advisor.py
├── resume_rewriter.py
├── interview_generator.py
├── section_detector.py
├── *_analyzer.py
├── templates/
│   ├── index.html
│   ├── base.html
│   └── result.html
├── static/
│   ├── css/style.css
│   └── js/{script.js,result.js}
├── tests/
├── docs/
├── requirements.txt
└── uploads/
```

## Application Workflow

1. The user uploads a PDF or DOCX resume.
2. The user supplies a target job description.
3. `/upload` validates the request and extracts text.
4. Existing analyzer modules inspect the resume.
5. ATS matching and weighted scoring are calculated.
6. Resume evidence, advisor recommendations, and interview questions are assembled.
7. The dashboard renders the complete analysis.
8. The user can open the Rewriter, prepare for interviews, and download a PDF report.

## Resume Parsing

PDF text is extracted with PyPDF2. DOCX text is extracted from `word/document.xml` using the standard library ZIP and XML modules. Unsupported extensions, malformed files, empty files, insufficient extracted text, and oversized requests receive user-facing errors.

## ATS Analysis

The ATS pipeline has two existing layers:

- `ats_engine.py` detects supported technical skills in the resume and job description, including related-skill handling.
- `score_engine.py` calculates the existing 100-point weighted result.

Current score categories are Skills 40, Projects 15, Experience 15, Education 10, Sections 10, and Formatting 10. This is a deterministic analysis, not a claim about how a specific commercial ATS evaluates resumes.

## Job Description Matching

The system reports skills found in both the resume and JD as matched. JD requirements not supported by resume text remain missing. A missing skill is never presented as a skill the candidate already possesses.

## Resume Evidence

`resume_evidence.py` records values with their type, section, source text, and source metadata where supported. Evidence includes skills, technologies, projects, experience, education, certifications, achievements, languages, metrics, and dates. This evidence is used to keep recommendations, rewrites, and interview questions grounded.

## Resume Advisor

`resume_advisor.py` returns structured recommendations with title, description, priority, section, source, evidence, JD relevance, and factual-safety metadata. Recommendations are ordered HIGH, MEDIUM, then LOW and distinguish unsupported JD requirements from confirmed resume evidence.

## Skills Intelligence

The dashboard separates:

- **Resume Skills:** skills explicitly found in resume evidence.
- **JD-Matched Skills:** supported skills found in both resume and JD.
- **Missing JD Skills:** JD requirements not currently supported by the resume.
- **Evidence-Backed Skills:** technologies with supporting resume evidence.

Duplicate values are normalized for display, and empty groups use intentional empty states.

## Resume Rewriter

The Rewriter is a local deterministic fallback. It improves wording, formatting, action verbs, and clarity without adding unsupported companies, roles, dates, technologies, metrics, degrees, certifications, projects, or achievements. Each candidate includes exact Original text, Improved text, source section, reason, keyword evidence, and factual-safety status.

## Interview Preparation

`interview_generator.py` produces structured questions from project, experience, technology, education, certification, achievement, JD-gap, and behavioral signals. Resume questions carry resume evidence. Missing JD requirements produce clarification questions rather than questions that assume unsupported experience.

## Resume Health Summary

The dashboard summarizes existing values only:

- ATS score.
- Matched and missing JD skill counts.
- HIGH-priority improvement count.
- Interview question count.
- Rewrite candidate count after the lazy rewrite scan runs.

No additional score or predictive model is introduced.

## PDF Report Generation

`POST /generate_pdf` receives the existing structured analysis payload and creates a ReportLab PDF. The report contains clear headings for Resume Overview, ATS / JD Match, Strengths, Priority Improvements, Skills, Interview Preparation, and supporting analysis. Rewriter content is not included because it is generated separately and is not part of the static PDF contract.

PDF values are escaped before ReportLab parsing, and empty sections use a readable fallback message.

## Empty/Error State Handling

The application handles:

- Missing, empty, malformed, unsupported, and oversized uploads.
- Missing or empty job descriptions.
- Invalid JSON and missing rewrite fields.
- Missing optional resume sections.
- No matched or missing skills.
- No recommendations, rewrite candidates, or interview questions.
- Missing session analysis data.
- PDF generation failures.

Errors are returned as concise JSON responses for API paths and readable messages in the browser.

## Security and Safety

- Upload extensions are allowlisted to PDF and DOCX.
- Filenames are normalized with `secure_filename`.
- Uploaded files are deleted after extraction.
- Upload requests are limited to 16 MB.
- Rewrite text has a 100,000-character limit.
- Dynamic dashboard values are HTML-escaped before rendering.
- PDF values are XML-escaped before ReportLab parsing.
- JD-only skills are not converted into resume evidence.
- Rule-based rewriting preserves factual boundaries.
- Resume text is processed as data; it is never executed.

## Testing

The current checkpoint is **134 tests passed, 0 failed**. Coverage includes pipeline integration, analyzers, edge-case resumes, evidence, advisor, rewriter safety, interview generation, Skills Intelligence, Resume Health, PDF output, malformed requests, oversized uploads, and hostile PDF values.

See [docs/TESTING.md](docs/TESTING.md) for the verified test categories and commands.

## How to Run

### Install

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Start

```powershell
python app.py
```

Open `http://127.0.0.1:5000/`.

### Test

```powershell
python -m pytest
```

## How to Use

1. Open the home page.
2. Upload a PDF or DOCX resume.
3. Paste a target job description.
4. Select **Analyze Resume**.
5. Review Resume Overview, ATS / JD Match, Strengths, Priority Improvements, and Skills.
6. Open Resume Details for extracted sections.
7. Review factual rewrite candidates.
8. Review grounded Interview Preparation questions.
9. Select **Download PDF** for the static report.

## Limitations

- Analysis is deterministic and vocabulary-based.
- Results depend on extractable text and recognizable section headings.
- The system does not replace professional recruiting judgment or a commercial ATS.
- No user accounts, persistent history, database, authentication, or multi-user storage are implemented.
- Rewriter results are previews; users should review them before use.
- PDF/DOCX extraction quality depends on document structure.

## Future Enhancements

- Optional persistent user accounts and analysis history.
- Stronger layout-aware PDF/DOCX extraction.
- Additional configurable skill vocabularies.
- More section-heading aliases.
- Accessibility and internationalization improvements.
- Rate limiting and production deployment controls.
- Optional provider integrations only with explicit safety and privacy controls.

## Conclusion

ResumeIQ is a transparent resume analysis workflow that turns a resume and target JD into explainable evidence, focused improvements, preparation questions, and a portable report. Its current design prioritizes deterministic behavior, factual safety, testability, and a coherent user journey.
