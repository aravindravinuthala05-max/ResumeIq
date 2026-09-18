# ResumeIQ Project Summary

## 1. Project Title

**ResumeIQ - AI Resume Intelligence Platform**

## 2. Subtitle and Motto

**Analyze - Improve - Get Hired**

The complete workflow is **ANALYZE -> UNDERSTAND -> IMPROVE -> PREPARE -> GET HIRED**.

## 3. Problem Statement

Resume review is often slow, fragmented, and difficult to verify. A candidate may receive a generic score without knowing which job requirements are supported, which are missing, what should be improved first, or how to prepare for an interview. Rewriting can also become unsafe if it introduces facts that are not present in the original resume.

## 4. Objective

ResumeIQ aims to extract structured resume information, compare it with a target job description, preserve source evidence, provide prioritized recommendations, offer fact-preserving rewrite previews, generate grounded interview questions, and present the result through a dashboard and PDF report.

## 5. Key Features

- PDF and DOCX resume text extraction.
- Contact, education, experience, project, certification, achievement, language, formatting, and section analysis.
- Weighted ATS-oriented score and category breakdown.
- JD-matched and missing skill lists.
- Resume Skills, JD-Matched Skills, Missing JD Skills, and Evidence-Backed Skills.
- Evidence-backed Resume Advisor recommendations.
- Rule-based, fact-preserving Resume Rewriter.
- Resume-grounded Interview Preparation.
- Resume Health summary.
- Continuous dashboard with anchor navigation.
- Backend-generated static PDF report.
- Empty and malformed-input handling.

## 6. Architecture

The Flask application receives the upload and job description, validates them, extracts resume text, runs independent analyzers, calculates skill matching and weighted scoring, builds resume evidence, generates advisor and interview data, and returns one JSON-safe analysis result. The browser renders that result in `result.html` and `result.js`. The browser can request lazy rewrite data from `/rewrite` and a static report from `/generate_pdf`.

## 7. Main Modules

- `app.py`: Flask routes, validation, orchestration, result assembly, and PDF generation.
- `resume_parser.py`: PDF text extraction.
- `section_detector.py`: section presence detection.
- `contact_analyzer.py`: contact details.
- `education_analyzer.py`: degree, institution, branch, CGPA, and related education values.
- `experience_analyzer.py`: roles, companies, and experience signals.
- `project_analyzer.py`: project counts and project categories.
- `certification_analyzer.py`: certification signals.
- `achievement_analyzer.py`: actions, metrics, and impact signals.
- `language_analyzer.py`: programming, scripting, markup, and natural-language signals.
- `formatting_analyzer.py`: length, bullets, dates, special characters, tables, and formatting quality.
- `ats_engine.py`: known skill extraction and resume/JD matching.
- `score_engine.py`: weighted ATS-oriented score.
- `resume_evidence.py`: traceable evidence records.
- `resume_advisor.py`: prioritized structured recommendations.
- `resume_rewriter.py`: local fact-preserving wording suggestions.
- `interview_generator.py`: resume- and JD-grounded questions.
- `templates/` and `static/`: dashboard presentation and interaction.

## 8. Technology Stack

- Python 3.8+
- Flask 3.0.0
- PyPDF2 3.0.1
- Python standard-library ZIP/XML handling for DOCX extraction
- ReportLab 4.2.5
- HTML, CSS, and vanilla JavaScript
- pytest 8.3.5

The current implementation is deterministic and rule-based. It does not depend on an external model or API.

## 9. Data Flow

1. The user uploads a PDF or DOCX resume and enters a job description.
2. Flask validates the file, extension, filename, and job description.
3. The resume is saved temporarily and text is extracted.
4. The temporary upload is removed after extraction.
5. Section detection and independent analyzers process the text.
6. Skill matching compares resume-supported skills with JD skills.
7. The weighted ATS score combines the existing score categories.
8. Resume Evidence records source-backed values.
9. The advisor and interview generator consume the structured result.
10. The browser renders the dashboard and can request rewrite or PDF data.

## 10. ATS Functionality

The ATS implementation has two layers. `ats_engine.py` detects known skills in the resume and job description and returns matched and missing skills. `score_engine.py` calculates the existing weighted result using Skills 40, Projects 15, Experience 15, Education 10, Sections 10, and Formatting 10. The score is a deterministic project score, not a claim about a commercial ATS.

## 11. Evidence System

Resume Evidence stores values with their type, section, source text, and source metadata where supported. It can cover skills, technologies, projects, experience, education, certifications, achievements, languages, metrics, and dates. This evidence supports explainable Skills Intelligence, recommendations, rewrite metadata, and interview questions.

## 12. Resume Advisor

The advisor uses missing skills, formatting issues, achievements, detected sections, matched skills, score information, job-description relevance, and resume evidence. It returns recommendations with title, description, priority, section, source, evidence, and safety information. Recommendations are presented with HIGH, MEDIUM, and LOW priorities.

## 13. Resume Rewriter

The Rewriter is a local deterministic fallback loaded through `/rewrite`. It keeps the exact original text, makes limited wording or formatting improvements, records the source section and evidence, and checks factual tokens. Unsupported companies, roles, dates, technologies, metrics, degrees, certifications, projects, or achievements must not be added.

## 14. Interview Preparation

`interview_generator.py` creates questions from projects, experience, supported technologies, education, certifications, achievements, JD gaps, resume evidence, and behavioral signals. Resume-grounded questions retain evidence metadata. Missing JD requirements become clarification questions and are not treated as confirmed candidate experience.

## 15. Skills Intelligence

The dashboard separates four concepts:

- **Resume Skills:** skills found in resume evidence.
- **JD-Matched Skills:** skills supported by both the resume and JD.
- **Missing JD Skills:** JD requirements not currently supported by the resume.
- **Evidence-Backed Skills:** technologies with supporting resume evidence.

This separation prevents a job requirement from being displayed as a candidate fact.

## 16. PDF and Report

`POST /generate_pdf` receives the existing structured analysis payload. ReportLab creates a static report with Resume Overview, ATS / JD Match, Strengths, Priority Improvements, Skills, Interview Preparation, and supporting analysis headings. The rewriter is generated through a separate lazy endpoint and is not part of the existing static PDF contract.

## 17. Safety and Validation

- Only PDF and DOCX extensions are accepted.
- Filenames are normalized with `secure_filename`.
- Upload requests are limited to 16 MB.
- Uploaded files are removed after extraction.
- Empty or insufficient extracted text is rejected.
- Empty job descriptions are rejected.
- Invalid JSON and invalid rewrite data return errors.
- Dashboard values are escaped before rendering.
- PDF values are XML-escaped before ReportLab parsing.
- Resume text is processed as data and never executed.
- JD-only skills are not converted into resume evidence.
- Rewrite output is checked for factual safety.

## 18. Testing

The verified project status is **134 tests passed, 0 tests failed**. Tests cover pipeline integration, analyzers, edge-case resumes, evidence, advisor behavior, rewriter safety and quality, interview generation, Skills Intelligence, Resume Health, dashboard integration, malformed requests, oversized uploads, hostile values, and PDF output.

## 19. Current Limitations

The system depends on extractable text and recognizable headings. Its skill vocabulary and rules are deterministic, so unusual wording or complex document layouts may not be fully interpreted. There is no persistent resume history, user authentication, database-backed account system, or deployment layer in the current scope. The result is decision support and does not replace professional recruiting judgment.

## 20. Future Scope

Possible future work includes authentication, persistent history, stronger layout-aware document extraction, more heading aliases, internationalization, rate limiting, privacy controls, and carefully controlled optional integrations. Any future enhancement should preserve source evidence and factual-safety boundaries.

## 21. Final One-Paragraph Explanation

ResumeIQ is a Flask-based, deterministic resume intelligence platform that takes a PDF or DOCX resume and a target job description, extracts and analyzes the resume, calculates a transparent ATS-oriented score, separates matched and missing skills, preserves source evidence, creates prioritized advisor recommendations, offers fact-preserving rewrite previews, generates grounded interview questions, and presents the result through a unified dashboard and static PDF report. Its central design principle is ANALYZE -> UNDERSTAND -> IMPROVE -> PREPARE -> GET HIRED, with validation and evidence used to keep the feedback explainable and factually controlled.
