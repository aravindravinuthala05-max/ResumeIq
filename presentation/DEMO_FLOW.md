# ResumeIQ Live Demo Flow

## Preparation

- Start the app with `python app.py`.
- Open `http://127.0.0.1:5000/`.
- Keep one realistic student/developer resume and one realistic software-engineering JD ready.
- Use a resume containing education, projects, Python/Flask/SQL skills, and at least one measurable result.
- Use a JD containing matching skills and at least one unsupported skill such as AWS or Docker.

## Exact Demo Sequence

### 1. Open ResumeIQ
- **Click:** Open the local ResumeIQ URL.
- **Show:** Landing page and product title.
- **Say:** “This is the ResumeIQ upload and analysis application.”

### 2. Show Landing Page
- **Click:** Nothing yet.
- **Show:** Upload area, JD field, and Analyze Resume button.
- **Say:** “The user provides both the resume and the target role.”

### 3. Upload Realistic Resume
- **Click:** Select the prepared PDF or DOCX in the upload area.
- **Show:** Selected filename.
- **Say:** “This resume contains education, project, skill, and evidence content.”

### 4. Add Realistic Software-Engineering JD
- **Click:** Job Description textarea.
- **Show:** Paste the prepared JD.
- **Say:** “The JD includes both supported and unsupported requirements.”

### 5. Click Analyze Resume
- **Click:** Analyze Resume.
- **Show:** Processing state, then the result dashboard.
- **Say:** “The Flask backend extracts text and runs the deterministic analysis pipeline.”

### 6. Show Overview
- **Click:** Overview or remain at the top.
- **Show:** Resume Overview card.
- **Say:** “The overview gives a quick summary before detailed sections.”

### 7. Show ATS Score
- **Click:** ATS / JD Match anchor.
- **Show:** Circular ATS score and breakdown.
- **Say:** “This is the existing weighted ATS result, not a new dashboard score.”

### 8. Show JD Matched/Missing Skills
- **Click:** Skills anchor.
- **Show:** JD-Matched Skills and Missing JD Skills.
- **Say:** “Matched skills are supported by both sources; missing skills are not confirmed candidate skills.”

### 9. Show Strengths
- **Click:** Strengths anchor.
- **Show:** Evidence-backed strength cards.
- **Say:** “These strengths come from resume evidence and supported JD relevance.”

### 10. Show Priority Improvements
- **Click:** Priority Improvements anchor.
- **Show:** HIGH and MEDIUM recommendation cards.
- **Say:** “The advisor keeps priority, section, evidence, and JD relevance visible.”

### 11. Show Skills Intelligence
- **Click:** Skills anchor.
- **Show:** Resume Skills, JD-Matched Skills, Missing JD Skills, and Evidence-Backed Skills.
- **Say:** “These groups prevent confusion between resume facts and JD-only requirements.”

### 12. Show Resume Details
- **Click:** Resume Details or Education, Experience, or Projects navigation.
- **Show:** Extracted contact, education, experience, projects, certifications, achievements, languages, and formatting.
- **Say:** “Detailed analyzer output remains available in a secondary area.”

### 13. Open Rewriter
- **Click:** Rewriter anchor or Open rewriter.
- **Show:** Loading message, then rewrite cards.
- **Say:** “The rewriter loads lazily through the existing local rule-based endpoint.”

### 14. Show ORIGINAL
- **Click:** Scroll to a rewrite card.
- **Show:** Original column.
- **Say:** “This is the exact source text selected for rewriting.”

### 15. Show IMPROVED
- **Click:** Keep the same card visible.
- **Show:** Improved column and factual-safety label.
- **Say:** “The improvement changes wording, not the underlying facts.”

### 16. Verify Improved Content Does Not Invent Facts
- **Click:** Compare Original and Improved visually.
- **Show:** Existing technologies, dates, and metrics remain unchanged.
- **Say:** “JD-only skills are not inserted, and unsafe factual changes are rejected.”

### 17. Open Interview Preparation
- **Click:** Interview anchor.
- **Show:** Numbered question list.
- **Say:** “Questions are generated from resume and job-description evidence.”

### 18. Show Resume/JD-Grounded Questions
- **Click:** Scroll through two or three questions.
- **Show:** Project, technical, education, or experience labels.
- **Say:** “Each resume-grounded question includes evidence metadata.”

### 19. Show JD-Gap Question
- **Click:** Locate the JD gap question.
- **Show:** Resume Gap label and clarification wording.
- **Say:** “The system asks whether the candidate has experience not reflected in the resume; it does not assume that experience.”

### 20. Download PDF
- **Click:** Download Report or Download PDF.
- **Show:** Browser download response.
- **Say:** “The backend generates a static analysis PDF.”

### 21. Open PDF
- **Click:** Open the downloaded PDF.
- **Show:** Resume Overview, ATS / JD Match, Strengths, Priority Improvements, Skills, and Interview Preparation headings.
- **Say:** “The report is readable, valid, and contains the major analysis sections.”

### 22. Return to Dashboard
- **Click:** Return to the result page.
- **Show:** Dashboard still available.
- **Say:** “The dashboard remains the interactive workspace; the PDF is the portable report.”

### 23. Finish With Conclusion
- **Click:** Nothing.
- **Show:** Final dashboard or title.
- **Say:** “ResumeIQ connects analysis, evidence, improvement, preparation, and reporting in one deterministic workflow.”

## DO NOT DEMO RANDOM FEATURES

Use only the safest, most complete features:

- Landing upload flow.
- ATS / JD Match.
- Resume Health.
- Skills Intelligence.
- Evidence-backed Strengths.
- Priority Improvements.
- Resume Details.
- Rewriter Original/Improved comparison.
- Interview Preparation and JD-gap question.
- PDF download and headings.

Avoid exploratory paths, direct API payload inspection, and unsupported claims about external AI.
