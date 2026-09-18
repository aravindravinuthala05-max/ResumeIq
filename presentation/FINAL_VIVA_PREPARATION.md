# ResumeIQ Final Viva Preparation

Short answers are provided so they can be spoken clearly during a viva.

## A. Basic Project Questions

### Q1. What is ResumeIQ?
ResumeIQ is a deterministic resume intelligence platform. It analyzes a resume against a target job description and provides matching, evidence, improvements, interview preparation, and a PDF report.

### Q2. What is the project motto?
ANALYZE -> UNDERSTAND -> IMPROVE -> PREPARE -> GET HIRED.

### Q3. What input does the application need?
It needs a PDF or DOCX resume and a non-empty job description.

### Q4. What output does it produce?
It produces structured analysis shown in a dashboard, plus a downloadable static PDF report.

## B. Problem Statement and Motivation

### Q5. What problem are you solving?
Resume review is slow and often disconnected from the target role. Candidates need to understand supported skills, missing requirements, improvement priorities, and interview topics.

### Q6. Why did you choose this project?
Resume review is a practical problem where explainable, evidence-based feedback is useful for students and job seekers.

### Q7. What is the main objective?
The objective is to connect resume extraction, job matching, factual improvement, interview preparation, and reporting in one workflow.

### Q8. Why is generic keyword matching insufficient?
It can show a word match without explaining its source, whether the candidate supports it, or what action should follow.

## C. Architecture

### Q9. What is the high-level architecture?
Flask receives and validates the upload, the parser extracts text, analyzers build structured results, scoring and matching run, evidence and recommendations are created, and the dashboard or PDF presents the result.

### Q10. What does app.py do?
It defines Flask routes, validates requests, orchestrates analyzers, assembles the JSON-safe result, serves the pages, and generates the PDF response.

### Q11. Why use independent analyzer modules?
They keep responsibilities small, make behavior easier to test, and allow one section to be analyzed without mixing all logic together.

### Q12. What is the role of section_detector.py?
It detects whether expected resume sections such as education, experience, projects, skills, and certifications are present.

### Q13. Why does the browser use a structured result object?
A structured result lets the frontend render overview, scores, skills, details, advice, interviews, and health values from the same analysis.

## D. Resume Parsing

### Q14. How is a PDF parsed?
PyPDF2 extracts text from PDF pages, after which the application analyzes the extracted text.

### Q15. How is a DOCX parsed?
The application reads the DOCX ZIP package and extracts paragraph text from `word/document.xml` using the standard library.

### Q16. What happens if extraction produces too little text?
The upload is rejected with an error saying that enough text could not be extracted.

### Q17. Does the application preserve the uploaded file?
The uploaded file is saved temporarily for extraction and removed in a `finally` block.

### Q18. What sections are analyzed?
The project analyzes contact, education, experience, projects, certifications, achievements, languages, formatting, and detected sections.

## E. ATS

### Q19. How does the ATS work?
The ATS layer detects known skills in the resume and JD, while the weighted score combines skills, projects, experience, education, sections, and formatting.

### Q20. What are the weighted score categories?
The current score uses Skills 40, Projects 15, Experience 15, Education 10, Sections 10, and Formatting 10.

### Q21. Is the ATS score the same as JD matching?
No. The ATS score summarizes several resume dimensions. JD matching focuses on skill overlap and missing requirements.

### Q22. Is the score a commercial ATS prediction?
No. It is the project's deterministic ATS-oriented score, not a claim about any particular commercial system.

### Q23. What does the score breakdown show?
It shows the contribution of the supported categories so the result is easier to interpret.

## F. Job Description Matching

### Q24. What is a matched skill?
It is a known skill found in both the resume text and the job description.

### Q25. What is a missing JD skill?
It is a known JD requirement that is not currently supported by the resume text.

### Q26. What happens when a skill appears only in the JD?
It remains a missing or unsupported requirement. It is not added to resume skills or evidence.

### Q27. Why can related technologies be displayed carefully?
The matching rules can distinguish related technologies from exact matches, so the display does not overstate support.

### Q28. What if the JD is empty?
The upload route rejects an empty job description instead of producing a misleading comparison.

## G. Evidence Extraction

### Q29. What is Resume Evidence?
It is structured information containing a value, type, section, source text, and source metadata where available.

### Q30. Why is evidence important?
Evidence connects a result to the resume source and helps prevent unsupported advice, rewrites, and interview assumptions.

### Q31. What can evidence contain?
It can include skills, technologies, projects, experience, education, certifications, achievements, languages, metrics, and dates.

### Q32. How does evidence help the dashboard?
It supports the Skills Intelligence groups, strengths, advisor explanations, rewrite metadata, and grounded interview questions.

## H. Resume Advisor

### Q33. What does the Resume Advisor do?
It creates structured recommendations based on missing skills, formatting issues, achievements, sections, matched skills, score information, and evidence.

### Q34. What information does an advisor recommendation contain?
It can contain a title, description, priority, section, source, evidence, JD relevance, and factual-safety information.

### Q35. What do HIGH, MEDIUM, and LOW mean?
They are the priorities assigned by the existing advisor rules to help the user decide what to address first.

### Q36. Can the advisor tell the user to claim a missing skill?
No. A missing JD skill is described as unsupported or requiring clarification, not as a fact the candidate should claim.

## I. Resume Rewriter

### Q37. What is the Resume Rewriter?
It is a local rule-based feature that improves wording and formatting while preserving facts already present in the resume.

### Q38. Why is the ORIGINAL text shown?
It lets the user compare the proposed improvement with the exact source text.

### Q39. How does the rewriter avoid hallucinating information?
It uses existing resume facts, checks factual tokens, and rejects or reverts unsafe proposed changes.

### Q40. Can it add a technology from the JD?
No. A JD-only technology cannot be safely inserted as candidate experience.

### Q41. Is the rewriter loaded in the first analysis response?
No. Rewriter results are loaded lazily through the separate `/rewrite` endpoint when the section is opened.

## J. Interview Generator

### Q42. What sources create interview questions?
Projects, experience, matched technologies, education, certifications, achievements, JD gaps, resume evidence, and behavioral signals.

### Q43. How are project questions grounded?
They use the project name and information from the project's resume evidence.

### Q44. How are questions for missing skills written?
They ask whether the candidate has practical experience that is not reflected in the resume. They do not assume the experience exists.

### Q45. What is the purpose of metadata labels?
Labels show whether a question is about a project, evidence, a JD match, a JD gap, or another category.

## K. Frontend and Dashboard

### Q46. What technologies are used in the frontend?
The project uses HTML templates, CSS, and vanilla JavaScript.

### Q47. What does the result dashboard show?
It shows the overview, health, ATS and JD match, strengths, priorities, Skills Intelligence, details, rewriter, interview preparation, and report action.

### Q48. Why use anchor navigation?
It gives the user a predictable way to move through a long continuous report.

### Q49. What is Resume Health?
It summarizes existing values such as ATS score, JD match counts, priority count, interview count, and rewrite count after lazy loading.

## L. PDF Generation

### Q50. How is the PDF generated?
The browser sends the existing analysis payload to `/generate_pdf`, and ReportLab creates a static PDF.

### Q51. Which sections are in the PDF?
The report includes headings for Resume Overview, ATS / JD Match, Strengths, Priority Improvements, Skills, Interview Preparation, and supporting analysis.

### Q52. Why is rewriter content not in the PDF?
The rewriter is loaded separately and is not part of the existing static PDF data contract.

## M. Testing

### Q53. What is the verified test result?
The verified status is 134 tests passed and 0 tests failed.

### Q54. What does 134 tests passed mean?
It means the current verified test suite completed successfully across normal flows, analyzers, edge cases, safety behavior, dashboard integration, and PDF behavior.

### Q55. What areas are tested?
Pipeline integration, analyzers, edge cases, evidence, advisor, rewriter quality and safety, interview generation, Skills Intelligence, health values, dashboard behavior, malformed input, and PDF output.

### Q56. Why are tests important for this project?
They make deterministic behavior reproducible and help detect regressions in factual safety and input handling.

## N. Security and Validation

### Q57. How are file types validated?
The application allows only PDF and DOCX extensions after securing the filename.

### Q58. How are oversized uploads handled?
Flask limits requests to 16 MB and returns a clear error for an oversized upload.

### Q59. How are malformed uploads handled?
Extraction errors are caught, the temporary file is removed, and the user receives a concise error response.

### Q60. How is unsafe HTML prevented in dashboard output?
Dynamic dashboard values are escaped before being inserted into the page.

### Q61. How is unsafe content handled in the PDF?
PDF values are XML-escaped before ReportLab parses them.

### Q62. Does the application execute resume text?
No. Resume text is processed as data and is never executed.

## O. Limitations

### Q63. What are the current limitations?
The system depends on extractable text, recognizable headings, and deterministic skill vocabularies. It has no persistent user history or authentication and does not replace professional recruiting judgment.

### Q64. What if a resume has no experience?
The experience analyzer returns an empty or unavailable result, and the dashboard can still display other sections and recommendations.

### Q65. What if a resume has no projects?
Project analysis can be empty, while the remaining analyzers, score categories, evidence, and dashboard still operate.

### Q66. What if a section heading is unusual?
Detection may not recognize it, which is a limitation of keyword-based section detection.

### Q67. Does the score guarantee an interview?
No. It is an explainable project score and should support review, not predict a hiring decision.

## P. Future Improvements

### Q68. What would you improve first?
I would add persistent history and authentication, stronger document layout extraction, more heading aliases, rate limiting, and clearer privacy controls.

### Q69. Why is there no database now?
The current scope focuses on a single analysis workflow and does not require persistent user history. A database is a future enhancement.

### Q70. Why not use an external API?
The current design prioritizes privacy, reproducibility, low operational complexity, and factual control.

### Q71. What would improve with a real AI model?
A carefully controlled model could help with richer wording or document interpretation, but it would require privacy, validation, cost, reproducibility, and factual-safety controls.

### Q72. Would you replace the deterministic rules?
No. I would keep deterministic validation and evidence boundaries around any optional future model feature.

## Q. Difficult Examiner Questions

### Q73. Why did you choose a rule-based approach?
It is explainable, reproducible, easy to test locally, and appropriate when factual accuracy matters more than open-ended generation.

### Q74. Why call it an AI Resume Intelligence Platform without a model?
Here, intelligence means combining multiple analysis signals into useful decisions. The implementation is deterministic and transparent rather than dependent on a generative service.

### Q75. How do you avoid inventing resume information?
Resume evidence is tied to source text, JD-only requirements remain unsupported, and rewrite output is checked before it is shown.

### Q76. How does the system distinguish resume evidence from JD requirements?
Evidence is built from resume text and analyzer outputs. JD skills are used for comparison, but a JD-only skill is not added to resume evidence.

### Q77. What happens when the resume has no experience and no projects?
Those analyzers return empty results, the related score categories reflect the input, and the dashboard still shows available sections with appropriate empty states.

### Q78. How do you handle an empty job description?
The upload route checks the trimmed value and rejects the request before analysis.

### Q79. What is the complete data flow?
The browser uploads the file and JD, Flask validates them, text is extracted, analyzers run, ATS and weighted scoring run, evidence and recommendations are assembled, the JSON result is rendered, and the browser can request a PDF or lazy rewrite.

### Q80. How do you know the result is safe to show?
The system validates input, limits size and extensions, catches extraction errors, escapes dashboard and PDF values, and tests malformed and hostile values.

### Q81. Why is the PDF static?
The PDF is generated from the existing analysis payload. The lazily loaded rewriter has a separate contract, so it is not silently added to the static report.

### Q82. What would you say if an examiner asks whether the score is objective?
It is objective within the project's fixed rules and inputs, but it is not a universal measure of candidate quality or a commercial ATS guarantee.

### Q83. How do you defend the claim that the system is explainable?
Each major output has a rule, category, source text, evidence record, or structured metadata that can be inspected.

### Q84. What is the strongest contribution of the project?
It connects matching, evidence, advice, safe wording improvement, interview preparation, and reporting while preserving factual boundaries.
