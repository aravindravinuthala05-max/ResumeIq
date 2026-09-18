# ResumeIQ Viva Questions and Answers

## Core Questions

1. **What is ResumeIQ?**  
   ResumeIQ is a deterministic resume intelligence platform that analyzes a resume against a job description and provides evidence-backed improvements and interview preparation.

2. **Why did you choose this project?**  
   Resume review is common, but candidates often receive generic feedback. I wanted to build one explainable workflow for analysis, improvement, and preparation.

3. **What is the problem statement?**  
   Candidates need to understand ATS alignment, missing JD requirements, resume weaknesses, and interview topics without changing or inventing their facts.

4. **What are the main objectives?**  
   Extract resume information, compare it with a JD, preserve evidence, prioritize improvements, generate safe rewrites, prepare questions, and create a report.

5. **What is the overall architecture?**  
   Flask validates and orchestrates the pipeline. Parsing, detection, analyzers, ATS, evidence, advisor, rewriter, interview, dashboard, and PDF modules each have separate responsibilities.

6. **Why did you use Flask?**  
   Flask is lightweight, easy to understand, and suitable for connecting Python analysis functions with web routes and JSON responses.

7. **Why did you use Python?**  
   Python provides simple text processing, regular expressions, PDF support, testing tools, and clear modular code.

8. **What does the frontend use?**  
   It uses HTML templates, CSS, and vanilla JavaScript. A frontend framework is not required for the current dashboard.

9. **How is a resume parsed?**  
   PDF text is extracted with PyPDF2. DOCX text is read from the document XML inside the DOCX ZIP package.

10. **How are PDF and DOCX different in this project?**  
    PDFs use PyPDF2 page extraction. DOCX files are ZIP containers, so the application reads `word/document.xml` with standard-library XML tools.

11. **What is section detection?**  
    It is a deterministic check for headings and keywords such as Education, Experience, Projects, Skills, and Certifications.

12. **What is ATS analysis?**  
    It is an existing weighted analysis that combines skills, projects, experience, education, section presence, and formatting into a score from the current scoring engine.

13. **What is JD matching?**  
    JD matching compares known skills in the resume and job description and returns matched and missing skills.

14. **Is ATS the same as JD matching?**  
    No. JD matching focuses on skill overlap. ATS scoring also includes resume structure and other analyzer outputs.

15. **What is Resume Evidence?**  
    It is a collection of traceable records containing a value, type, section, source text, and source metadata where supported.

16. **Why is evidence important?**  
    Evidence shows where a result came from and helps prevent unsupported recommendations or rewrites.

17. **What is Skills Intelligence?**  
    It separates resume skills, JD-matched skills, missing JD skills, and evidence-backed technologies.

18. **What happens to a JD-only skill?**  
    It stays a missing or unsupported requirement. The system does not present it as a confirmed candidate skill.

19. **What does the Resume Advisor do?**  
    It creates structured recommendations with priority, section, evidence, source, and JD relevance.

20. **How are priorities assigned?**  
    Existing advisor rules classify recommendations as HIGH, MEDIUM, or LOW. No new scoring system is added for advice.

21. **What is the Resume Rewriter?**  
    It is a local rule-based provider that improves wording while preserving facts already present in the resume.

22. **How does the rewriter preserve facts?**  
    It keeps exact Original text, applies limited wording rules, checks factual tokens, and reverts unsafe proposed text to the original.

23. **Can the rewriter add AWS from a JD?**  
    No. If AWS is only in the JD, the rewrite cannot claim AWS experience.

24. **What is the Interview Generator?**  
    It creates questions from projects, technologies, experience, education, certifications, achievements, JD gaps, and generic behavioral prompts.

25. **How are project questions grounded?**  
    Each project question uses the project name and technologies found on that project's source line.

26. **How are JD-gap questions written?**  
    They ask whether the candidate has experience not currently reflected in the resume. They do not assume the experience exists.

27. **What is Resume Health?**  
    It is a concise summary of existing values such as ATS score, match counts, priority count, interview count, and rewrite count.

28. **How is the PDF generated?**  
    The browser sends the existing analysis payload to `/generate_pdf`, and ReportLab creates a static PDF with clear headings.

29. **Why is there no rewriter content in the PDF?**  
    Rewriter results are generated lazily through a separate endpoint and are not part of the existing static PDF contract.

30. **Why did you choose a deterministic/rule-based approach?**  
    It is explainable, reproducible, easy to test, and safer for a project where factual accuracy is important.

31. **Why did you not use an external LLM?**  
    The project requirements prioritized privacy, reproducibility, no external dependency, and factual safety. The current scope can meet those goals with deterministic rules.

32. **How do you prevent invented facts?**  
    Evidence is tied to source text, recommendations distinguish JD gaps, and rewrite output is checked for unsupported factual tokens.

33. **How do you validate uploads?**  
    The application checks that a file exists, has a filename, uses PDF or DOCX, stays within the 16 MB limit, and produces enough extracted text.

34. **How are invalid requests handled?**  
    API routes return JSON errors for missing fields, invalid JSON, malformed files, oversized input, and invalid rewrite data.

35. **How is HTML-like content handled?**  
    Dashboard values are HTML-escaped, and PDF values are XML-escaped before ReportLab parses them.

36. **How are temporary files handled?**  
    Uploaded files are saved only for extraction and removed in a `finally` block.

37. **How did you test the system?**  
    I used pytest for pipeline, analyzer, evidence, advisor, rewriter, interview, dashboard, edge-case, security, and PDF tests.

38. **What is the current test result?**  
    The verified checkpoint is 134 tests passed and 0 failed.

39. **What browser testing was performed?**  
    The landing page, dashboard, Health, Skills, Rewriter, Interview, PDF response, navigation, and empty states were manually verified with a browser automation smoke flow.

40. **What are the main limitations?**  
    The system depends on extractable text and recognizable headings, uses deterministic vocabularies, has no persistent user accounts, and does not replace professional recruiting judgment.

41. **What is the future scope?**  
    Future options include history, authentication, stronger layout-aware extraction, more heading aliases, internationalization, rate limiting, and carefully controlled optional integrations.

## DIFFICULT QUESTIONS EXAMINERS MAY ASK

42. **Why do you call it AI Resume Intelligence if it is rule-based?**  
    Here, intelligence means combining multiple analysis signals into useful decisions. The implementation is transparent and deterministic rather than generated by an external AI model.

43. **What is the difference between ATS and JD matching?**  
    JD matching reports skill overlap. ATS scoring combines that skill result with projects, experience, education, sections, and formatting.

44. **How do you prevent hallucination or invented resume facts?**  
    The system uses source evidence, marks JD-only skills as unsupported, and validates rewrite output before showing it.

45. **Why did you not use an LLM?**  
    An LLM would add privacy, cost, availability, and reproducibility concerns. A deterministic first version is easier to explain and validate for a student project.

46. **How does the rewriter preserve factual accuracy?**  
    It performs limited replacements, keeps the source line as Original, tracks section and keyword evidence, and reverts unsafe changes.

47. **How are interview questions generated?**  
    The generator reads structured resume text and existing analyzer values, gives higher priority to project and matched evidence, and adds safe JD-gap and behavioral questions.

48. **What happens if the JD contains a skill missing from the resume?**  
    The skill appears in Missing JD Skills and can produce a clarification question. It is not added to resume evidence or confirmed skills.

49. **How did you test security?**  
    I tested missing, empty, malformed, unsupported, oversized, invalid JSON, hostile HTML-like, Unicode, and missing-JD inputs. I also verified no traceback was returned to the client.

50. **What would you improve first in a production version?**  
    I would add authentication, persistent history, rate limiting, stronger document layout extraction, and privacy controls before adding optional external integrations.
