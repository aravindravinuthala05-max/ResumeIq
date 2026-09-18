# Presentation Script

## Opening

Good morning everyone. Today I am presenting my final-year project, ResumeIQ, an AI Resume Intelligence Platform. The main idea is simple: a user uploads a resume and a target job description, and ResumeIQ helps them analyze, improve, and prepare for that role. The current system is deterministic and rule-based. It does not use ChatGPT or any external LLM.

## SLIDE 1 — Title

**WHAT TO SAY:**
ResumeIQ stands for a resume intelligence workflow. It follows the path Analyze, Understand, Improve, Prepare, and Get Hired. The system combines resume parsing, ATS-oriented analysis, evidence, recommendations, rewriting, interview preparation, and PDF reporting in one application.

## SLIDE 2 — Introduction

**WHAT TO SAY:**
A resume contains many useful facts, but it is not always easy for a candidate to understand which facts matter for a particular job. ResumeIQ gives one guided report instead of making the user use many separate tools. The important point is that the feedback is explainable because it comes from deterministic rules and extracted evidence.

## SLIDE 3 — Problem Statement

**WHAT TO SAY:**
Manual resume review takes time, and generic keyword matching does not explain enough. A candidate may not know which JD skills are supported, which are missing, or which improvements matter most. Also, an unsafe rewriter could accidentally add a technology or achievement that the candidate never had. ResumeIQ addresses these problems together.

## SLIDE 4 — Existing System

**WHAT TO SAY:**
In a common workflow, a candidate may check an ATS score in one place, get resume advice somewhere else, and prepare for interviews separately. These outputs may not share the same evidence. ResumeIQ brings these activities into one report while keeping each calculation transparent and testable.

## SLIDE 5 — Proposed System

**WHAT TO SAY:**
The proposed system accepts a resume and job description, extracts the text, analyzes different sections, calculates the existing ATS result, and builds an evidence-aware report. The user can then see strengths, priority improvements, skills, safe rewrite suggestions, interview questions, and a downloadable PDF.

## SLIDE 6 — Objectives

**WHAT TO SAY:**
The main objectives were to extract useful resume data, compare it with a target job, preserve traceable evidence, and give practical next steps. Another important objective was factual safety. The system should improve presentation without inventing companies, dates, technologies, metrics, or qualifications.

## SLIDE 7 — Technology Stack

**WHAT TO SAY:**
The backend uses Python and Flask. PyPDF2 extracts PDF text, and the standard library handles DOCX XML content. ReportLab creates the PDF report. The frontend uses normal HTML, CSS, and JavaScript, and pytest is used for automated testing. We intentionally did not depend on an external AI service.

## SLIDE 8 — System Architecture

**WHAT TO SAY:**
The architecture is modular. Flask validates the request and starts the pipeline. The parser extracts text, the section detector and analyzers create structured results, and the ATS and score engines calculate matching and scoring. Evidence, advisor, and interview modules then use those results. Finally, the dashboard and PDF layers present them.

## SLIDE 9 — Application Workflow

**WHAT TO SAY:**
The user first uploads a PDF or DOCX resume and pastes a job description. After analysis, the dashboard starts with the overview and ATS match. It then moves through strengths, priority improvements, skills, resume details, rewriting, and interview preparation. The final action is downloading the report.

## SLIDE 10 — Core Modules

**WHAT TO SAY:**
There is one main Flask orchestration module and several focused modules. The analyzers cover contact, education, experience, projects, certifications, achievements, languages, formatting, and sections. Other modules handle ATS matching, evidence, advice, rewriting, interview questions, and PDF generation. This makes the system easier to test than one large function.

## SLIDE 11 — ATS & Job Description Analysis

**WHAT TO SAY:**
The existing ATS result is a weighted score using skills, projects, experience, education, sections, and formatting. JD matching is a separate view that identifies matched and missing skills. If AWS appears only in the job description, it remains a missing or unsupported requirement. It is never displayed as a confirmed candidate skill.

## SLIDE 12 — Resume Evidence & Skills Intelligence

**WHAT TO SAY:**
Resume Evidence stores values together with their type, section, source text, and source information where available. The Skills section uses that information to separate resume skills, JD-matched skills, missing JD skills, and evidence-backed technologies. This is useful because it shows not only a label, but also where the support comes from.

## SLIDE 13 — Resume Advisor & Rewriter

**WHAT TO SAY:**
The advisor produces structured recommendations with priority and evidence. For example, a missing JD skill is described as a requirement not currently supported by the resume, not as something the user should falsely claim. The rewriter is rule-based. It can improve wording and formatting, but its safety check rejects unsupported factual tokens and keeps the original when necessary.

## SLIDE 14 — Interview Preparation

**WHAT TO SAY:**
Interview questions are generated from project, experience, technology, education, certification, achievement, JD-gap, and behavioral signals. Resume questions include resume evidence. For missing skills, the system asks a clarification question such as whether the candidate has practical experience that is not reflected. It does not assume that experience exists.

## SLIDE 15 — Dashboard & PDF Report

**WHAT TO SAY:**
The result page is a continuous dashboard with anchor navigation. Resume Health summarizes existing values such as the ATS score, match counts, priorities, interview count, and rewrite count after loading. The PDF is generated on the backend with clear headings. It is a static analysis report and does not include lazy rewriter content.

## SLIDE 16 — Testing, Security & Results

**WHAT TO SAY:**
The verified test result is 134 tests passed and zero failed. The tests cover normal resumes, unusual structures, malformed uploads, evidence, advisor behavior, rewriter safety, interview questions, Skills Intelligence, Health, and PDF output. Security checks include upload limits, extension validation, escaped dashboard content, and escaped PDF values.

## SLIDE 17 — Conclusion & Future Scope

**WHAT TO SAY:**
To conclude, ResumeIQ gives a complete and explainable path from resume upload to job preparation. It is not a replacement for human judgment, but it makes the review process more focused and safer. Future work could add user history, authentication, stronger document layout extraction, and optional integrations with clear privacy controls. Thank you.

## Closing

Thank you for listening. I am happy to explain the architecture, testing, or factual-safety design in more detail.
