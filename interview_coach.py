"""Evidence-grounded preparation metadata layered over legacy interview questions."""

import re


def _title(value):
    return str(value or "Resume").replace("_", " ").title()


def _prepare_topics(item):
    evidence = [str(value) for value in item.get("evidence", []) if value]
    category = item.get("category", "")
    if category == "JD gap":
        return ["the skill is not evidenced in your resume", "core concepts", "a small truthful practice exercise"]
    if category.startswith("Project"):
        return ["problem statement", "technical approach", "design decisions", "real challenges and outcomes"]
    if category == "Technical":
        return ["where the skill appears in your resume", "what you implemented", "why you chose the approach", "one real problem you solved"]
    if category == "Behavioral":
        return ["a real situation", "your actions", "the supported outcome"]
    return evidence[:2] + ["your actual responsibilities and outcomes"]


def _answer_structure(item):
    if item.get("category") == "JD gap":
        return ["State that the skill is not evidenced in the resume.", "Explain what you would learn first.", "Describe a small, truthful way to practise it."]
    return ["State the supported work or context.", "Explain your actual approach.", "Describe one real decision or challenge.", "Mention a result only if it is in the resume."]


def _gap_guidance(item):
    """Give a practical route for a JD skill without implying experience."""
    skill = str((item.get("evidence") or ["this requirement"])[0])
    return {
        "what_to_learn_first": [f"Learn the core purpose and vocabulary of {skill}.", "Understand one basic workflow and its trade-offs."],
        "how_to_practise": [f"Complete one small, truthful practice task using {skill}.", "Keep notes on what you built and one problem you solved."],
        "interview_preparation": ["State that the skill is not currently represented in your resume.", "Explain the fundamentals you have started learning and the practice task you actually completed."],
    }


def _priority(item):
    if item.get("category") == "JD gap" or item.get("jd_match"):
        return "High"
    if item.get("category") in {"Project", "Project deep-dive", "Technical", "Experience"}:
        return "Medium"
    return "Low"


def _difficulty(item):
    if item.get("category") in {"Project deep-dive", "Technical"} and item.get("jd_match"):
        return "Hard"
    if item.get("category") in {"Project", "Technical", "Experience", "JD gap"}:
        return "Medium"
    return "Easy"


def _coach_item(item):
    category = item.get("category", "Resume-Based")
    source = item.get("source", "resume")
    evidence = list(item.get("evidence") or [])
    if source == "job_description":
        reason = "This is a job-description skill gap and is not evidenced in your resume."
        status = "Not evidenced in resume"
    elif source == "generic":
        reason = "This prepares a general communication skill without asserting a resume fact."
        status = "General preparation"
    else:
        reason = f"This is grounded in {_title(category)} evidence from your resume."
        if item.get("jd_match"):
            reason += " The evidence is also relevant to the provided job description."
        status = "Resume evidence"
    guidance = _gap_guidance(item) if source == "job_description" else {}
    return {
        "question": item["question"], "category": category, "difficulty": _difficulty(item),
        "priority": _priority(item), "source": source, "section": _title(category),
        "evidence": evidence, "jd_match": bool(item.get("jd_match")), "reason": reason,
        "status": status, "what_interviewer_tests": "How clearly you can explain supported work and reasoning.",
        "what_to_prepare": _prepare_topics(item), "answer_structure": _answer_structure(item),
        **guidance,
        "follow_ups": (["Why did you choose that approach?", "What would you improve next?"]
                       if category in {"Project", "Project deep-dive"} else []), "fact_safe": True,
    }


def build_interview_coach(interview_questions, semantic_matches, matched_skills, missing_skills):
    """Return a JSON-safe coaching layer; never alters legacy questions or skills."""
    legacy = [item for item in (interview_questions or []) if isinstance(item, dict)]
    # Gap preparation is safety-critical; it must not disappear simply because
    # higher-priority resume questions filled the initial display limit.
    selected = [item for item in legacy if item.get("category") == "JD gap"]
    selected.extend(item for item in legacy if item.get("category") != "JD gap")
    known_gaps = {str(value).casefold() for item in selected if item.get("category") == "JD gap" for value in item.get("evidence", [])}
    for skill in missing_skills or []:
        if str(skill).casefold() not in known_gaps:
            selected.insert(0, {
                "question": f"What would you learn first about {skill} for this role?",
                "category": "JD gap", "source": "job_description", "evidence": [skill],
                "jd_match": False, "fact_safe": True,
            })
    items = [_coach_item(item) for item in selected[:12]]
    semantic = (semantic_matches or {}).get("matches", []) if isinstance(semantic_matches, dict) else []
    for match in semantic:
        if match.get("label") != "Related Semantic Match" or not match.get("evidence"):
            continue
        requirement = str(match.get("requirement"))
        items.append({
            "question": f"How does the resume evidence relate to {requirement}?",
            "category": "Technical", "difficulty": "Hard", "priority": "High", "source": "semantic_match",
            "section": _title(match.get("section")), "evidence": [match["evidence"]], "jd_match": True,
            "reason": "Your resume evidence is semantically related to this job-description requirement.",
            "status": "Related semantic evidence", "what_interviewer_tests": "Your ability to connect supported work to role requirements.",
            "what_to_prepare": [requirement, "the evidence you listed", "relevant fundamentals"],
            "answer_structure": ["State the supported evidence.", "Explain its actual approach.", "Do not claim an unlisted skill."],
            "follow_ups": [], "fact_safe": True,
        })
    items = items[:15]
    topics = [str(skill) for skill in (matched_skills or [])[:4]] + [str(skill) for skill in (missing_skills or [])[:3]]
    roadmap = [
        {"title": "Resume Fundamentals", "topics": [item["evidence"][0] for item in items if item["source"] == "resume" and item["evidence"]][:3]},
        {"title": "JD Technical Requirements", "topics": [str(skill) for skill in (matched_skills or [])[:4]]},
        {"title": "Project Deep Dive", "topics": [item["evidence"][0] for item in items if item["category"].startswith("Project") and item["evidence"]][:3]},
        {"title": "Skill Gaps", "topics": [str(skill) for skill in (missing_skills or [])[:3]]},
        {"title": "Behavioral Preparation", "topics": ["real situations", "clear communication"]},
    ]
    return {"questions": items, "roadmap": roadmap, "high_priority_topics": topics[:6], "fact_safe": True}
