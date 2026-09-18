# ResumeIQ: Examiner Quick Answers

Use these answers as spoken prompts. The documented verified status is **134 tests passed, 0 failed**.

## Project, purpose, and technology

1. **Question:** What is ResumeIQ?  
   **Short answer:** ResumeIQ is a deterministic, rule-based platform that analyzes a resume against a target job description.  
   **If examiner asks deeper:** It provides ATS-oriented scoring, skills comparison, evidence-backed advice, factual rewrite previews, interview questions, and a PDF report.

2. **Question:** Why did you build it?  
   **Short answer:** I built it to make resume review more structured, explainable, and useful for a target role.  
   **If examiner asks deeper:** It shows what is supported, what is missing, and what the user can improve without inventing facts.

3. **Question:** What problem does it solve?  
   **Short answer:** It reduces the difficulty of manually comparing a resume with a job description.  
   **If examiner asks deeper:** It organizes matching, evidence, prioritized improvements, interview preparation, and reporting in one workflow.

4. **Question:** Why did you choose this project?  
   **Short answer:** Resume improvement is a practical student and job-seeker problem where factual safety matters.  
   **If examiner asks deeper:** That made it a good fit for explainable deterministic analysis rather than uncontrolled text generation.

5. **Question:** What technologies did you use?  
   **Short answer:** Python, Flask, HTML, CSS, vanilla JavaScript, PyPDF2, ReportLab, and pytest.  
   **If examiner asks deeper:** DOCX extraction uses Python standard-library ZIP/XML handling.

6. **Question:** Why Flask?  
   **Short answer:** Flask is lightweight and suitable for a focused request-response web application.  
   **If examiner asks deeper:** It cleanly handles routes, validation, JSON responses, templates, and the PDF response in this scope.

7. **Question:** What is the high-level architecture?  
   **Short answer:** Browser upload and JD go to Flask, which extracts text, runs analyzers, builds evidence and results, then returns a dashboard payload.  
   **If examiner asks deeper:** The browser stores the payload in session storage; rewriting is lazy through `/rewrite` and PDF generation uses `/generate_pdf`.

8. **Question:** Why use separate analyzer modules?  
   **Short answer:** They keep each responsibility small and easier to test.  
   **If examiner asks deeper:** Contact, education, experience, projects, formatting, and other results can be developed and checked independently.

## Parsing and validation

9. **Question:** How does resume parsing work?  
   **Short answer:** The application extracts text first, then analyzers inspect that text.  
   **If examiner asks deeper:** PDF text uses PyPDF2, while DOCX text is read from `word/document.xml`.

10. **Question:** What formats are supported?  
    **Short answer:** PDF and DOCX.  
    **If examiner asks deeper:** Other extensions are rejected before analysis.

11. **Question:** What happens if extraction fails?  
    **Short answer:** The upload returns a clear error instead of producing an unreliable analysis.  
    **If examiner asks deeper:** Malformed files, empty files, and text extraction with fewer than 100 characters are rejected.

12. **Question:** How do you handle invalid uploads?  
    **Short answer:** The route checks that a file exists, has a filename, has an allowed extension, and can be extracted.  
    **If examiner asks deeper:** Filenames are normalized with `secure_filename`, and temporary uploaded files are removed after extraction.

13. **Question:** How do you handle oversized uploads?  
    **Short answer:** Flask limits upload requests to 16 MB.  
    **If examiner asks deeper:** The application returns a readable 413 error for a larger request.

14. **Question:** What happens if there is no JD?  
    **Short answer:** The request is rejected because comparison without a job description would be misleading.  
    **If examiner asks deeper:** The upload route checks the trimmed JD before starting analysis.

15. **Question:** What happens when there is no experience?  
    **Short answer:** The experience result can be empty, but the other analyzers and dashboard continue working.  
    **If examiner asks deeper:** The related score contribution reflects the available input rather than inventing experience.

16. **Question:** What happens when there are no projects?  
    **Short answer:** Project analysis can be empty while the rest of the workflow still runs.  
    **If examiner asks deeper:** The dashboard uses intentional empty states for optional missing content.

17. **Question:** What happens when there are no certifications?  
    **Short answer:** Certifications are treated as optional and shown as empty when not detected.  
    **If examiner asks deeper:** Their absence does not stop parsing, evidence construction, or report generation.

## ATS, matching, and evidence

18. **Question:** What is ATS?  
    **Short answer:** ATS means Applicant Tracking System; here it refers to an ATS-oriented resume analysis score.  
    **If examiner asks deeper:** It is not a simulation or guarantee of a specific commercial ATS.

19. **Question:** How does your ATS work?  
    **Short answer:** It uses fixed rules and a weighted score across skills, projects, experience, education, sections, and formatting.  
    **If examiner asks deeper:** The weights are Skills 40, Projects 15, Experience 15, Education 10, Sections 10, and Formatting 10.

20. **Question:** What is JD matching?  
    **Short answer:** It compares known skills found in the resume with known skills found in the target job description.  
    **If examiner asks deeper:** Skills present in both are matched; JD requirements without resume support remain missing.

21. **Question:** How are skills matched?  
    **Short answer:** The rules detect supported technical skill vocabulary in both texts.  
    **If examiner asks deeper:** Related-skill handling is careful so the display does not overstate resume support.

22. **Question:** What happens when a JD contains a missing skill?  
    **Short answer:** It is shown as a missing JD skill, not as a candidate skill.  
    **If examiner asks deeper:** The advisor says to add it only when the candidate genuinely has verified experience.

23. **Question:** What is resume evidence?  
    **Short answer:** It is structured information linked to what was found in the resume.  
    **If examiner asks deeper:** Evidence can record value, type, section, source text, and source metadata for skills, projects, experience, metrics, and more.

24. **Question:** Why is evidence important?  
    **Short answer:** It makes recommendations and questions traceable to the resume.  
    **If examiner asks deeper:** It also prevents JD-only requirements from being treated as resume facts.

25. **Question:** How do you prove recommendations are evidence-backed?  
    **Short answer:** Recommendation objects include fields such as source, evidence, section, priority, JD relevance, and factual safety.  
    **If examiner asks deeper:** The dashboard can render that structured information instead of relying on unexplained advice.

26. **Question:** How does the dashboard work?  
    **Short answer:** It renders the structured analysis result stored in browser session storage.  
    **If examiner asks deeper:** It displays overview, health, ATS/JD match, strengths, priorities, skills, details, rewriting, interviews, and report actions.

## Advisor, Rewriter, and interviews

27. **Question:** What is Resume Advisor?  
    **Short answer:** It is the deterministic component that creates prioritized resume-improvement recommendations.  
    **If examiner asks deeper:** It uses missing skills, evidence, formatting findings, achievements, section status, matched skills, and score information.

28. **Question:** What is Resume Rewriter?  
    **Short answer:** It is a local rule-based preview that improves wording and clarity while preserving resume facts.  
    **If examiner asks deeper:** It shows exact Original and Improved text with source section, reason, keywords, and factual-safety status.

29. **Question:** How does rewriting stay safe?  
    **Short answer:** It checks factual tokens and does not add unsupported facts.  
    **If examiner asks deeper:** Unsupported companies, roles, dates, technologies, metrics, degrees, certifications, projects, and achievements are prevented or reverted.

30. **Question:** Can the rewriter add skills that the candidate does not have?  
    **Short answer:** No. A JD-only skill cannot be inserted as candidate experience.  
    **If examiner asks deeper:** The feature is a fact-preserving wording improvement, not a way to create credentials.

31. **Question:** What is Interview Generator?  
    **Short answer:** It generates up to 15 structured interview questions from resume and JD signals.  
    **If examiner asks deeper:** Its sources include projects, experience, technologies, education, certifications, achievements, JD gaps, and behavioral signals.

32. **Question:** How are interview questions selected?  
    **Short answer:** Rules prioritize available resume evidence and relevant matched or missing JD skills.  
    **If examiner asks deeper:** Questions include category, source, evidence, JD-match status, priority, and factual-safety metadata.

33. **Question:** How are questions written for a missing skill?  
    **Short answer:** They ask whether the candidate has practical experience not reflected in the resume.  
    **If examiner asks deeper:** They do not assume unsupported experience exists.

34. **Question:** How does the system avoid hallucination?  
    **Short answer:** It is rule-based and keeps outputs anchored to structured resume evidence.  
    **If examiner asks deeper:** JD-only skills remain unsupported, and rewrite validation rejects unsupported factual changes.

## Report, safety, and testing

35. **Question:** How does PDF generation work?  
    **Short answer:** The browser sends the current analysis payload to `/generate_pdf`, and ReportLab creates a PDF.  
    **If examiner asks deeper:** It includes overview, ATS/JD match, strengths, priorities, skills, interview preparation, and supporting analysis.

36. **Question:** Why is Rewriter content not in the PDF?  
    **Short answer:** Rewriter data is loaded separately and is outside the static PDF payload contract.  
    **If examiner asks deeper:** This keeps the report based on the original structured analysis result.

37. **Question:** How do you handle malicious-looking text?  
    **Short answer:** Resume text is treated as data and never executed.  
    **If examiner asks deeper:** Upload validation, controlled parsing, and output escaping reduce unsafe input handling risks.

38. **Question:** How do you prevent HTML injection?  
    **Short answer:** Dynamic dashboard values are HTML-escaped before rendering.  
    **If examiner asks deeper:** PDF values are also XML-escaped before ReportLab parses them.

39. **Question:** How did you test the project?  
    **Short answer:** I used pytest across pipeline behavior, analyzers, edge cases, evidence, safety, dashboard behavior, and PDF output.  
    **If examiner asks deeper:** Tests also cover malformed requests, oversized uploads, and hostile PDF values.

40. **Question:** What does “134 tests passed, 0 failed” mean?  
    **Short answer:** It is the documented verified checkpoint for the current test suite.  
    **If examiner asks deeper:** It means 134 tests completed successfully with no test failures in that verified run.

## Design decisions and difficult questions

41. **Question:** Why did you choose a deterministic, rule-based architecture?  
    **Short answer:** It is explainable, reproducible, testable, and appropriate when factual accuracy matters.  
    **If examiner asks deeper:** Fixed rules make the same input produce inspectable behavior without depending on a remote provider.

42. **Question:** Is this actually AI?  
    **Short answer:** The implementation is deterministic and rule-based, not a trained or generative model.  
    **If examiner asks deeper:** The word intelligence describes combining analysis signals into useful guidance, while the technical behavior remains transparent rules.

43. **Question:** Your project is called AI Resume Intelligence Platform. Where is the AI?  
    **Short answer:** In the current implementation, the intelligence is rule-based analysis and decision support, not an external generative model.  
    **If examiner asks deeper:** I describe it accurately as deterministic resume intelligence and do not claim model integration.

44. **Question:** Why should I call this intelligent if it is rule-based?  
    **Short answer:** It combines multiple signals into context-aware, useful actions instead of simply displaying keywords.  
    **If examiner asks deeper:** It links matching, evidence, prioritization, factual rewriting, interview preparation, and reporting in one workflow.

45. **Question:** Why did you not use an external LLM?  
    **Short answer:** I prioritized privacy, reproducibility, low operational complexity, and factual control for this version.  
    **If examiner asks deeper:** Any future provider integration would still need evidence boundaries, validation, privacy controls, and testing.

46. **Question:** Why did you not train your own model?  
    **Short answer:** The current problem is well served by transparent rules, and a trained model would require suitable labeled data and additional evaluation.  
    **If examiner asks deeper:** A model would not remove the need for factual validation or explainability.

47. **Question:** What happens if your rules are wrong?  
    **Short answer:** The result can be incomplete or inaccurate within the known vocabulary, so it should support review rather than replace judgment.  
    **If examiner asks deeper:** The modular design and tests make rules easier to inspect, correct, and extend.

48. **Question:** Can your system understand every type of resume?  
    **Short answer:** No. It depends on extractable text, recognizable headings, and supported vocabulary.  
    **If examiner asks deeper:** Complex layouts and unusual headings are explicit limitations and future improvement areas.

49. **Question:** Can it guarantee ATS acceptance?  
    **Short answer:** No. The score is a project-specific deterministic indicator, not a commercial ATS guarantee.  
    **If examiner asks deeper:** Different organizations use different systems, rules, and hiring criteria.

50. **Question:** Can it guarantee a job?  
    **Short answer:** No. It helps improve preparation and resume review but cannot predict hiring outcomes.  
    **If examiner asks deeper:** Hiring includes many factors outside the resume analysis.

51. **Question:** Why did you not use a database?  
    **Short answer:** The current scope is a single local analysis workflow without persistent history or accounts.  
    **If examiner asks deeper:** Persistent history, authentication, and multi-user storage are sensible future enhancements.

52. **Question:** What happens if the resume contains false information?  
    **Short answer:** The application analyzes the submitted text; it cannot independently verify real-world claims.  
    **If examiner asks deeper:** It avoids adding new claims, but the candidate remains responsible for the truth of the source resume.

53. **Question:** What is the biggest limitation of the current system?  
    **Short answer:** It relies on text extraction, section headings, and a deterministic skill vocabulary.  
    **If examiner asks deeper:** It also has no persistent accounts or history and does not replace professional recruiting judgment.

54. **Question:** What was the hardest technical part?  
    **Short answer:** Keeping multiple outputs consistent with resume evidence and factual boundaries.  
    **If examiner asks deeper:** The solution was to build structured evidence and reuse it in advice, rewriting, and interview questions.

55. **Question:** What would you change if you had more time?  
    **Short answer:** I would improve layout-aware extraction, add more section aliases and skill vocabularies, and add secure persistent history.  
    **If examiner asks deeper:** I would also add rate limiting, accessibility and internationalization improvements, and carefully controlled optional provider integrations.
