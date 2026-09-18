# ResumeIQ: Final Demo and Viva Guide

Use this guide with the verified project checkpoint: **134 tests passed, 0 failed**.

## 1. Five-minute preparation checklist

### Files to have ready

- This project folder, including `app.py`, `requirements.txt`, `templates/`, `static/`, and `presentation/ResumeIQ_Final_Presentation.pptx`.
- One readable PDF or DOCX resume with meaningful text. Prefer one containing education, projects, skills, and at least one measurable result.
- One realistic target job description containing a few skills present in the resume and at least one skill not supported by it.
- The existing presentation and, if desired, a previously downloaded report. Do not edit the PPTX or application code immediately before presenting.

### Start and check

1. Open PowerShell in the project folder.
2. Activate the existing environment if it is not active:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Start the application using the repository command:

   ```powershell
   python app.py
   ```

4. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/).
5. Confirm that the ResumeIQ landing page shows the upload area, Job Description field, and **Analyze Resume** button.
6. Run one complete analysis before the presentation. Check that the dashboard, Rewriter, Interview Preparation, and **Download PDF** work.

### Do not change before presenting

- Do not change application source code, dependencies, test files, or the existing PPTX.
- Do not use an untested resume or a JD with no recognizable skills at the last minute.
- Do not make claims beyond the deterministic, rule-based implementation.

## 2. Exact live demo sequence

### 1. Open ResumeIQ

- **Click:** Open `http://127.0.0.1:5000/`.
- **Point at:** The ResumeIQ title.
- **Say:** “This is ResumeIQ, a resume analysis workflow for comparing a resume with a target job description.”
- **Examiner should understand:** The demo begins with a local working web application.

### 2. Explain the landing page

- **Click:** Nothing yet.
- **Point at:** Upload Resume, Job Description, and **Analyze Resume**.
- **Say:** “The user provides the resume and the target role, so the analysis is role-specific.”
- **Examiner should understand:** Both inputs are required for a meaningful comparison.

### 3. Upload the resume

- **Click:** **Drag & Drop Your Resume** or click to browse; choose the prepared PDF or DOCX.
- **Point at:** The selected filename.
- **Say:** “The application accepts PDF and DOCX resumes and extracts their text for analysis.”
- **Examiner should understand:** The source is an actual resume document, not manually invented dashboard data.

### 4. Add the job description

- **Click:** The Job Description box and paste the prepared JD.
- **Point at:** A few required skills in the pasted JD.
- **Say:** “I use a JD with both supported requirements and a few gaps so the matching result is easy to interpret.”
- **Examiner should understand:** JD requirements are compared against resume evidence.

### 5. Analyze

- **Click:** **Analyze Resume**.
- **Point at:** The processing state, then the resulting dashboard.
- **Say:** “Flask validates the request, extracts text, runs the analyzers, calculates matching and scoring, and returns one structured result.”
- **Examiner should understand:** The result follows a defined local processing pipeline.

### 6. Explain ATS / JD Match

- **Click:** **ATS / JD Match** in the report navigation.
- **Point at:** The overall score and the Skills, Projects, Experience, Education, Sections, and Formatting breakdown.
- **Say:** “This is a deterministic ATS-oriented score. It summarizes fixed weighted categories; it is not a commercial ATS prediction.”
- **Examiner should understand:** ATS scoring and JD matching are explainable project rules, not hiring prediction.

### 7. Explain strengths

- **Click:** **Strengths**.
- **Point at:** The strength cards and their supporting evidence.
- **Say:** “These strengths are based on supported resume evidence that is relevant to the JD.”
- **Examiner should understand:** Strengths are tied to resume facts, not generic praise.

### 8. Explain priority improvements

- **Click:** **Priority Improvements**.
- **Point at:** HIGH, then MEDIUM priority recommendations.
- **Say:** “The advisor orders recommendations so the user can address the most important supported gaps first.”
- **Examiner should understand:** A missing skill is an unsupported JD requirement, not a claim about the candidate.

### 9. Open Skills

- **Click:** **Skills**.
- **Point at:** Resume Skills, JD-Matched Skills, Missing JD Skills, and Evidence-Backed Skills.
- **Say:** “These four groups separate what is in the resume, what matches the JD, what is missing, and what has supporting evidence.”
- **Examiner should understand:** The interface deliberately prevents JD-only skills from becoming resume facts.

### 10. Explain matched and missing skills

- **Click:** Remain in **Skills**.
- **Point at:** One matched skill and one missing JD skill.
- **Say:** “A matched skill appears in both sources. A missing skill appears in the JD but is not currently supported by this resume.”
- **Examiner should understand:** Matching is a comparison, not an assumption of competence.

### 11. Open Advisor

- **Click:** **Priority Improvements** or **Review improvements**.
- **Point at:** Priority, section, and evidence/source information on a recommendation.
- **Say:** “Resume Advisor creates structured recommendations with priority, section, source, evidence, JD relevance, and factual-safety metadata.”
- **Examiner should understand:** The recommendations are evidence-backed and ordered by rules.

### 12. Explain evidence-backed recommendations

- **Click:** Keep one recommendation visible.
- **Point at:** Its evidence and wording about an unsupported skill, if present.
- **Say:** “The recommendation tells the user to add a missing skill only if they genuinely have verified experience with it.”
- **Examiner should understand:** The system does not encourage fabricated content.

### 13. Open Rewriter

- **Click:** **Rewriter** or **Open rewriter**.
- **Point at:** The loading status, then a rewrite card.
- **Say:** “The rewriter is loaded on demand through the local rule-based rewrite endpoint.”
- **Examiner should understand:** Rewriting is separate from the main analysis and uses no external provider.

### 14. Explain ORIGINAL versus IMPROVED

- **Click:** None; keep one rewrite card visible.
- **Point at:** The **Original** and **Improved** columns.
- **Say:** “The original is the exact source text. The improved version makes wording clearer while retaining the supported facts.”
- **Examiner should understand:** The proposal is reviewable rather than a hidden replacement.

### 15. Explain safe rewriting and no invention

- **Click:** Keep the factual-safety label visible.
- **Point at:** The safety status and any supported keyword/evidence line.
- **Say:** “The rewriter must not add unsupported companies, roles, dates, technologies, metrics, degrees, certifications, projects, or achievements. Unsafe changes are reverted.”
- **Examiner should understand:** The rewriter is a factual preview, not free-form content generation.

### 16. Open Interview Preparation

- **Click:** **Interview** or **Prepare interview**.
- **Point at:** Two or three generated questions and their category/source labels.
- **Say:** “The questions are selected from project, experience, technology, education, certification, achievement, JD-gap, and behavioral signals.”
- **Examiner should understand:** Questions are grounded in the resume and comparison result.

### 17. Explain generated questions

- **Click:** Find a JD-gap question if the selected JD has a missing skill.
- **Point at:** Its clarification wording and evidence.
- **Say:** “For a missing JD skill, the question asks whether the candidate has experience not reflected in the resume; it does not assume that experience exists.”
- **Examiner should understand:** The interview feature remains fact-safe.

### 18. Generate and download the PDF

- **Click:** **Download PDF**.
- **Point at:** The download and, if time permits, open the PDF.
- **Say:** “The browser sends the existing analysis payload to the backend, which creates a ReportLab PDF.”
- **Examiner should understand:** The PDF is a portable static report containing the main analysis sections; rewrite content is separate and not in its static contract.

### 19. Finish with the overall workflow

- **Click:** Return to the dashboard top or leave the final report visible.
- **Point at:** The report navigation.
- **Say:** “ResumeIQ connects upload, analysis, evidence, focused improvement, safe rewriting, interview preparation, and reporting in one deterministic workflow.”
- **Examiner should understand:** The project has an end-to-end, explainable user journey.

## 3. Important things to demonstrate

| Area | Demonstrate | Key point to say |
| --- | --- | --- |
| ATS | Overall score and six weighted categories. | “It is a deterministic ATS-oriented project score, not a commercial ATS or hiring prediction.” |
| JD matching | One matched and one missing skill. | “JD-only skills remain unsupported.” |
| Resume evidence | Strength or advisor evidence metadata. | “Outputs are connected back to resume evidence.” |
| Skills | The four Skills groups. | “The groups distinguish facts, matches, gaps, and evidence.” |
| Advisor | A HIGH/MEDIUM recommendation. | “Recommendations show priority, section, source, evidence, and JD relevance.” |
| Rewriter | Original/Improved and factual-safety label. | “It improves wording without adding facts.” |
| Interview preparation | A project question and a JD-gap question. | “Questions are grounded; gaps use clarification questions.” |
| PDF report | Downloaded report headings. | “ReportLab produces a static, readable report from the analysis payload.” |
| Empty states | If available, use an intentionally sparse resume or point out the readable empty-state wording. | “Optional sections can be absent without breaking the analysis.” |
| Safety validation | PDF/DOCX allowlist, 16 MB limit, escaped output, and evidence boundary. | “Input is validated; dynamic HTML and PDF values are escaped; resume text is data, never executable.” |

## 4. If an examiner asks to change the resume

Do not edit facts live to make a result look better. Say: “I can demonstrate the safe workflow: I would update the source resume only with verified information, save it as PDF or DOCX, upload it again, and rerun the analysis against the same JD.”

If asked to add a missing JD skill, say: “I would add it only if the candidate has genuine, verifiable experience. Otherwise it should remain a gap.” Use the Rewriter only to show a preview; review and manually apply any approved wording outside the application.

## 5. If something fails during the demo

| Situation | Safe recovery |
| --- | --- |
| Flask does not start | In the project folder, activate the existing environment and run `python app.py`. Read the terminal error; if a dependency is missing, use the documented `pip install -r requirements.txt`, then start again. |
| Port 5000 is already in use | Stop the existing terminal process already running ResumeIQ with `Ctrl+C`, then run `python app.py` again. The current application is configured for port 5000. |
| Resume upload fails | Confirm that the file is a readable PDF or DOCX, has extractable text, is below 16 MB, and that a non-empty JD is pasted. Select the prepared backup resume and submit again. |
| Analysis appears to take time | Keep the page open while its progress state is visible. Wait for the analysis response; do not refresh during processing. |
| PDF generation fails | Return to the dashboard, confirm the analysis loaded, then click **Download PDF** once more. If it still fails, continue the demo with the dashboard and explain that the report endpoint creates the portable version from the displayed payload. |
| Browser page becomes stale | Return to `http://127.0.0.1:5000/`, re-upload the prepared resume, paste the prepared JD, and analyze again. |
| An unexpected section is empty | State that the system has intentional empty-state handling for missing optional sections. Use the visible sections, or rerun with the prepared resume that includes projects and skills. |

## 6. What not to say

- Do not say an LLM generated any result.
- Do not say ChatGPT, OpenAI, Gemini, Claude, or another external AI/LLM provider is connected or currently used.
- Do not claim that the score predicts ATS acceptance, interviews, hiring, or a job offer.
- Do not claim that the application generates candidate facts or fills missing skills automatically.
- Do not claim unsupported machine-learning models are running.
- Do not call a missing JD skill a candidate skill.
- Do not say every resume layout or section heading is understood perfectly.
- Do not call the PDF a record of Rewriter output; the Rewriter is generated separately and is not part of the static PDF contract.

## 7. Thirty-second project explanation

“ResumeIQ is a deterministic, rule-based resume intelligence platform. A user uploads a PDF or DOCX resume and adds a target job description. The Flask application extracts text, analyzes resume sections, calculates an ATS-oriented score, compares supported skills with the JD, and presents evidence-backed strengths and improvements. It also gives fact-preserving rewrite previews, grounded interview questions, and a downloadable PDF report. The key design principle is that missing JD skills remain gaps unless the candidate can verify them.”

## 8. One-minute project explanation

“I built ResumeIQ to make resume review more structured and explainable. The user uploads a PDF or DOCX resume and pastes a target job description. The backend validates the request, extracts resume text, and runs separate analyzers for contact details, education, experience, projects, certifications, achievements, languages, formatting, and sections. A deterministic ATS layer compares known skills and calculates a weighted score across skills, projects, experience, education, sections, and formatting.

The dashboard separates resume skills, JD matches, missing JD skills, and evidence-backed skills. The Resume Advisor prioritizes evidence-backed actions, while the Rewriter improves wording without adding facts. Interview Preparation turns resume evidence and JD gaps into questions, and the user can download a ReportLab PDF. The project is intentionally rule-based, which makes its behavior reproducible, testable, and safer for factual resume content.”

## 9. Two-minute technical explanation

“ResumeIQ uses Python, Flask, HTML, CSS, vanilla JavaScript, PyPDF2 for PDF text extraction, standard-library ZIP/XML handling for DOCX extraction, ReportLab for PDF output, and pytest for testing. The browser submits the resume and JD to the Flask `/upload` route. The route validates that a file exists, that the JD is not empty, that the extension is PDF or DOCX, and that the request is within the 16 MB limit. The file is stored temporarily for extraction and removed afterward.

The application then runs independent analyzers for contact information, education, experience, projects, certifications, achievements, languages, formatting, and section detection. `ats_engine.py` detects supported known skills in the resume and JD, including careful related-skill handling. `score_engine.py` calculates the fixed 100-point ATS-oriented result: Skills 40, Projects 15, Experience 15, Education 10, Sections 10, and Formatting 10. This score is transparent within the project rules, but it is not a commercial ATS prediction.

`resume_evidence.py` turns detected information into structured evidence with values, types, sections, source text, and metadata where available. The Resume Advisor uses that evidence, scores, formatting findings, missing skills, and section status to create prioritized recommendations. It explicitly says that a JD-only skill should be added only if the candidate genuinely has verified experience.

The Rewriter is a local deterministic feature accessed lazily through `/rewrite`. It shows exact Original and Improved text, checks factual tokens, and prevents unsupported companies, roles, dates, technologies, metrics, degrees, certifications, projects, and achievements from being added. The Interview Generator produces up to 15 questions from resume and JD signals; JD gaps become clarification questions rather than assumptions. The result payload is stored in browser session storage for rendering, and `/generate_pdf` creates a ReportLab report from that structured payload. Dynamic dashboard values are HTML-escaped and PDF values are XML-escaped. The documented verified status is 134 tests passed, 0 failed.”

## 10. Final closing statement

“ResumeIQ delivers an end-to-end, explainable resume-review workflow: it turns resume and job-description inputs into transparent matching, evidence-backed guidance, safe wording previews, interview preparation, and a portable report. Its current deterministic design prioritizes factual boundaries, reproducibility, and clear user decisions rather than unsupported claims about hiring outcomes.”
