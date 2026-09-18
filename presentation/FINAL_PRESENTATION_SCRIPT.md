# ResumeIQ Final Presentation Script

**Target duration:** 7-10 minutes

**Core workflow:** ANALYZE -> UNDERSTAND -> IMPROVE -> PREPARE -> GET HIRED

## Slide 1 - Title: ResumeIQ

**What I should say:**
ResumeIQ is my final-year project: a resume intelligence platform that takes a resume and a target job description, analyzes the match, suggests improvements, and prepares the candidate for an interview. The workflow is Analyze, Understand, Improve, Prepare, and Get Hired.

**Important point to emphasize:**
The current implementation is deterministic and rule-based. It does not depend on an external model or API.

**Approximate speaking time:** 20 seconds

## Slide 2 - Introduction

**What I should say:**
A resume contains useful information, but it is difficult to quickly tell which parts matter for a particular role. ResumeIQ brings resume analysis, job matching, improvement guidance, interview preparation, and reporting into one guided dashboard.

**Important point to emphasize:**
The feedback is explainable because it comes from extracted text, known rules, and stored evidence.

**Approximate speaking time:** 20 seconds

## Slide 3 - Problem Statement

**What I should say:**
Manual resume review takes time. A candidate may not know which job-description skills are supported, which are missing, or which improvements should come first. A rewriting tool can also become unsafe if it adds facts that were never in the resume. ResumeIQ addresses these problems together.

**Important point to emphasize:**
The goal is not just keyword matching. The system must show support, gaps, and safe next steps.

**Approximate speaking time:** 25 seconds

## Slide 4 - Existing System

**What I should say:**
In a typical workflow, a candidate may use one tool for an ATS score, another for resume advice, and another for interview questions. These tools may not share the same evidence. ResumeIQ combines the workflow so the outputs are connected and easier to inspect.

**Important point to emphasize:**
The project improves the review workflow without claiming to replace human judgment.

**Approximate speaking time:** 20 seconds

## Slide 5 - Proposed System

**What I should say:**
The proposed system accepts one resume and one target job description. It extracts the text, analyzes resume sections, calculates the existing ATS result, compares skills with the job description, and then presents evidence, recommendations, rewrite previews, interview questions, and a PDF report.

**Important point to emphasize:**
The user moves from diagnosis to action inside one continuous dashboard.

**Approximate speaking time:** 25 seconds

## Slide 6 - Objectives

**What I should say:**
My objectives were to extract useful information from PDF and DOCX resumes, compare resume-supported skills with a job description, preserve traceable evidence, prioritize improvements, provide safe rewrite previews, generate grounded interview questions, and deliver both a dashboard and a report.

**Important point to emphasize:**
Factual safety is a requirement across analysis, advice, rewriting, and interview preparation.

**Approximate speaking time:** 25 seconds

## Slide 7 - Technology Stack

**What I should say:**
The backend uses Python and Flask. PyPDF2 extracts PDF text, and the Python standard library reads DOCX XML inside the DOCX package. ReportLab generates the PDF. The frontend uses HTML, CSS, and JavaScript, and pytest verifies the behavior.

**Important point to emphasize:**
The stack is lightweight, local, reproducible, and rule-based.

**Approximate speaking time:** 20 seconds

## Slide 8 - System Architecture

**What I should say:**
Flask validates the request and orchestrates the pipeline. The parser extracts text, the section detector and analyzers build structured results, ATS matching finds supported and missing skills, and the score engine calculates the weighted score. Evidence, the advisor, interview generation, the dashboard, and the PDF layer consume those results.

**Important point to emphasize:**
Separate modules make the system easier to test and explain than one large function.

**Approximate speaking time:** 30 seconds

## Slide 9 - Application Workflow

**What I should say:**
The user uploads a PDF or DOCX resume and pastes a job description. ResumeIQ analyzes the input, shows the overview and ATS match, then moves through strengths, priority improvements, Skills Intelligence, resume details, rewriting, interview preparation, and the downloadable report.

**Important point to emphasize:**
The workflow follows ANALYZE -> UNDERSTAND -> IMPROVE -> PREPARE -> GET HIRED.

**Approximate speaking time:** 25 seconds

## Slide 10 - Core Modules

**What I should say:**
The main modules are the parser, section detector, independent analyzers, ATS engine, score engine, resume evidence builder, advisor, rewriter, interview generator, Flask routes, dashboard JavaScript, and PDF generator. Each module has a focused responsibility and contributes to the final analysis object.

**Important point to emphasize:**
The system composes deterministic outputs instead of using one opaque decision-maker.

**Approximate speaking time:** 25 seconds

## Slide 11 - ATS & Job Description Analysis

**What I should say:**
There are two related but separate results. The weighted ATS score combines skills, projects, experience, education, sections, and formatting. JD matching focuses on skill overlap. A skill found in both sources is matched; a JD-only skill remains missing and is not treated as a candidate skill.

**Important point to emphasize:**
ATS scoring and JD matching are not the same calculation.

**Approximate speaking time:** 30 seconds

## Slide 12 - Resume Evidence & Skills Intelligence

**What I should say:**
Resume Evidence stores values with their type, section, source text, and available source information. Skills Intelligence uses that evidence to show Resume Skills, JD-Matched Skills, Missing JD Skills, and Evidence-Backed Skills. This makes it clear where a result came from.

**Important point to emphasize:**
A requirement appearing only in the JD is never displayed as confirmed resume experience.

**Approximate speaking time:** 30 seconds

## Slide 13 - Resume Advisor & Rewriter

**What I should say:**
The Resume Advisor creates structured recommendations with priority, section, evidence, source, and JD relevance. The Rewriter is a local deterministic feature. It keeps the exact original text, proposes limited wording improvements, checks factual tokens, and rejects or reverts unsupported changes.

**Important point to emphasize:**
The rewriter improves presentation, not the candidate's facts.

**Approximate speaking time:** 30 seconds

## Slide 14 - Interview Preparation

**What I should say:**
Interview questions are generated from projects, experience, technologies, education, certifications, achievements, JD gaps, and behavioral signals. Resume-grounded questions carry evidence. A missing JD skill produces a clarification question about experience not reflected in the resume; it does not assume that experience exists.

**Important point to emphasize:**
The generator distinguishes a resume fact from a job requirement.

**Approximate speaking time:** 30 seconds

## Slide 15 - Dashboard & PDF Report

**What I should say:**
The result page is a continuous dashboard with anchor navigation. Resume Health summarizes existing values such as ATS score, match counts, priorities, interview count, and rewrite count after the rewriter is opened. The backend creates a static PDF with the main report headings. Rewriter content is loaded separately and is not part of that static PDF contract.

**Important point to emphasize:**
The dashboard is interactive; the PDF is the portable analysis report.

**Approximate speaking time:** 30 seconds

## Slide 16 - Testing, Security & Results

**What I should say:**
The verified checkpoint is 134 tests passed and 0 tests failed. The tests cover the pipeline, analyzers, edge cases, evidence, advisor, rewriter safety, interview generation, Skills Intelligence, health values, PDF output, malformed input, oversized uploads, and browser flow. The application also validates file type and size and escapes dashboard and PDF values.

**Important point to emphasize:**
The result is reproducible and tested, not an unsupported performance claim.

**Approximate speaking time:** 30 seconds

## Slide 17 - Conclusion & Future Scope

**What I should say:**
ResumeIQ connects resume analysis and job preparation in one explainable workflow. It helps a candidate understand alignment, decide what to improve, rewrite wording safely, and prepare for questions. Future work could add history, authentication, stronger document layout extraction, and carefully controlled integrations. The main principle remains Analyze, Understand, Improve, Prepare, and Get Hired.

**Important point to emphasize:**
ResumeIQ is a deterministic, evidence-aware foundation that supports human decision-making.

**Approximate speaking time:** 25 seconds

## Closing

Thank you. I am happy to explain the architecture, the evidence model, the safety checks, or the testing strategy.
