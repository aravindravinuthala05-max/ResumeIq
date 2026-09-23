"""Local, evidence-backed semantic matching for ResumeIQ.

This module deliberately produces relevance signals, never resume facts or ATS
scores.  The model is loaded from the local Sentence Transformers cache only;
deployment must provision it ahead of time.
"""

import re
from threading import Lock

from ats_engine import ALL_SKILLS, SKILL_ALIASES, _skill_present


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
# Validated against the real local MiniLM model: the representative positive
# data-analysis fixture scores 0.403 while the Android/cloud negative scores
# 0.104.  Keep a margin below the positive and well above the negative.
HIGH_RELEVANCE_THRESHOLD = 0.62
MEDIUM_RELEVANCE_THRESHOLD = 0.36
ELIGIBLE_SECTIONS = {"summary", "experience", "projects", "skills"}

_model = None
_model_error = None
_model_lock = Lock()


def model_status():
    """Return a JSON-safe availability state without exposing model internals."""
    model = _get_model()
    return {
        "available": model is not None,
        "model": MODEL_NAME,
        "reason": None if model is not None else _model_error or "Local semantic model is unavailable.",
    }


def _get_model():
    global _model, _model_error
    if _model is not None:
        return _model
    if _model_error is not None:
        return None
    with _model_lock:
        if _model is not None:
            return _model
        if _model_error is not None:
            return None
        try:
            from sentence_transformers import SentenceTransformer
            # Runtime must not reach the network.  Provisioning is an explicit
            # deployment step so the service remains private and predictable.
            _model = SentenceTransformer(MODEL_NAME, local_files_only=True)
        except Exception as error:  # Existing analysis remains available.
            _model_error = f"Local semantic model unavailable: {type(error).__name__}."
    return _model


def extract_jd_requirements(job_description):
    """Extract short, source-backed JD requirement phrases; never invent terms."""
    text = job_description if isinstance(job_description, str) else ""
    pieces = []
    for line in text.splitlines():
        pieces.extend(re.split(r"[;\u2022]|(?<=[.!?])\s+", line.strip()))
    requirements = []
    seen = set()
    cue = re.compile(r"\b(?:experience|skill|skills|required|requirement|proficien|knowledge|familiar|ability|develop|analysis|comput|deploy|api|cloud)\b", re.I)
    for piece in pieces:
        clean = re.sub(r"\s+", " ", piece).strip(" -:\t")
        if 3 <= len(clean) <= 220 and (cue.search(clean) or any(_skill_present(clean, skill) for skill in ALL_SKILLS)):
            key = clean.casefold()
            if key not in seen:
                seen.add(key)
                requirements.append({"requirement": clean, "source": "job_description", "type": "requirement"})
    for skill in ALL_SKILLS:
        if _skill_present(text, skill) and skill.casefold() not in seen:
            seen.add(skill.casefold())
            requirements.append({"requirement": skill, "source": "job_description", "type": "skill"})
    return requirements


def _evidence_items(resume_evidence):
    items = []
    seen = set()
    for group in (resume_evidence or {}).values():
        for item in group if isinstance(group, list) else []:
            if not isinstance(item, dict) or item.get("section") not in ELIGIBLE_SECTIONS:
                continue
            source_text = str(item.get("source_text") or "").strip()
            if not source_text:
                continue
            key = (source_text.casefold(), str(item.get("section")), str(item.get("type")))
            if key not in seen:
                seen.add(key)
                items.append({
                    "evidence": source_text,
                    "section": item["section"],
                    "type": item.get("type", "resume_evidence"),
                })
    return items


def _exact_source(requirement, items):
    for item in items:
        if _skill_present(item["evidence"], requirement):
            return item
    return None


def _label(score):
    if score >= HIGH_RELEVANCE_THRESHOLD:
        return "Related Semantic Match"
    if score >= MEDIUM_RELEVANCE_THRESHOLD:
        return "Related Semantic Match"
    return "No Meaningful Match"


def match_requirements_to_evidence(requirements, resume_evidence, *, exact_requirements=(), model=None):
    """Match JD requirements to supported evidence with one batched embedding pass.

    `exact_requirements` is derived by the existing ATS matcher.  It is only
    used to label an already supported lexical/alias match; it never changes
    the deterministic match lists or score.
    """
    requirements = [item for item in (requirements or []) if isinstance(item, dict) and item.get("requirement")]
    evidence_items = _evidence_items(resume_evidence)
    selected_model = model if model is not None else _get_model()
    status = model_status() if model is None else {"available": True, "model": "test-model", "reason": None}
    if not selected_model:
        return {"available": bool(selected_model), "model": status["model"], "reason": status["reason"], "matches": []}
    if not requirements:
        return {"available": True, "model": status["model"], "reason": None, "matches": []}
    if not evidence_items:
        return {
            "available": True,
            "model": status["model"],
            "reason": None,
            "matches": [
                {
                    "requirement": str(item["requirement"]),
                    "evidence": None,
                    "section": None,
                    "type": None,
                    "similarity": 0.0,
                    "label": "No Meaningful Match",
                }
                for item in requirements
            ],
        }

    requirement_texts = [str(item["requirement"]) for item in requirements]
    evidence_texts = [item["evidence"] for item in evidence_items]
    try:
        vectors = selected_model.encode(requirement_texts + evidence_texts, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)
        requirement_vectors = vectors[:len(requirement_texts)]
        evidence_vectors = vectors[len(requirement_texts):]
    except Exception as error:
        return {"available": False, "model": status["model"], "reason": f"Local semantic inference unavailable: {type(error).__name__}.", "matches": []}

    exact = {str(value).split(" (", 1)[0].casefold() for value in exact_requirements}
    matches = []
    for index, requirement in enumerate(requirements):
        scores = requirement_vectors[index] @ evidence_vectors.T
        best_index = int(scores.argmax())
        score = max(0.0, min(1.0, float(scores[best_index])))
        text = str(requirement["requirement"])
        exact_item = _exact_source(text, evidence_items) if text.casefold() in exact else None
        if exact_item:
            matches.append({"requirement": text, **exact_item, "similarity": 1.0, "label": "Exact Match"})
        elif score >= MEDIUM_RELEVANCE_THRESHOLD:
            matches.append({"requirement": text, **evidence_items[best_index], "similarity": round(score, 4), "label": _label(score)})
        else:
            matches.append({"requirement": text, "evidence": None, "section": None, "type": None, "similarity": round(score, 4), "label": "No Meaningful Match"})
    return {"available": True, "model": status["model"], "reason": None, "matches": matches}
