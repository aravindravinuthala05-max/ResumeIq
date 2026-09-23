import json

import numpy as np

from app import build_analysis_result
from resume_evidence import build_resume_evidence
from semantic_matcher import extract_jd_requirements, match_requirements_to_evidence


class FixtureEmbeddingModel:
    """Small deterministic encoder for semantic matcher safety tests."""

    def encode(self, texts, **_kwargs):
        vectors = []
        for text in texts:
            lowered = text.casefold()
            if any(term in lowered for term in ("data analysis", "numerical computing", "predictive", "pandas", "numpy")):
                vectors.append([1.0, 0.0, 0.0])
            elif any(term in lowered for term in ("python backend", "api", "flask")):
                vectors.append([0.0, 1.0, 0.0])
            else:
                vectors.append([0.0, 0.0, 1.0])
        return np.array(vectors, dtype=float)


def semantic_result(requirement, resume):
    return match_requirements_to_evidence(
        [{"requirement": requirement, "source": "job_description", "type": "requirement"}],
        build_resume_evidence(resume),
        model=FixtureEmbeddingModel(),
    )


def test_semantic_relatedness_preserves_project_evidence_provenance():
    result = semantic_result(
        "Experience with data analysis and numerical computing",
        "PROJECTS\nForecasting tool: Built predictive models using pandas and NumPy.",
    )

    match = result["matches"][0]
    assert result["available"] is True
    assert match["label"] == "Related Semantic Match"
    assert match["section"] == "projects"
    assert match["type"] in {"project", "project_detail", "technology"}
    assert "predictive models" in match["evidence"]
    assert 0 <= match["similarity"] <= 1
    json.dumps(result)


def test_unrelated_education_and_contact_never_produce_semantic_evidence():
    for resume in (
        "EDUCATION\nB.Tech in Computer Science, State University",
        "CONTACT\nexample@gmail.com\n+91 555 010 1234",
    ):
        result = semantic_result("Python backend development", resume)
        match = result["matches"][0]
        assert match["label"] == "No Meaningful Match"
        assert match["evidence"] is None
        assert match["section"] is None


def test_exact_match_uses_existing_ats_signal_without_creating_a_skill():
    evidence = build_resume_evidence("SKILLS\nPython")
    result = match_requirements_to_evidence(
        [{"requirement": "python", "source": "job_description", "type": "skill"}],
        evidence,
        exact_requirements=["python"],
        model=FixtureEmbeddingModel(),
    )

    match = result["matches"][0]
    assert match["label"] == "Exact Match"
    assert match["evidence"] == "Python"


def test_jd_only_skill_remains_missing_and_ats_score_is_unchanged(monkeypatch, complete_resume):
    import app as application

    job_description = "Python backend development with React and Kubernetes"
    baseline = build_analysis_result(complete_resume, job_description, "resume.pdf")
    monkeypatch.setattr(
        application,
        "match_requirements_to_evidence",
        lambda *_args, **_kwargs: {"available": False, "model": "test", "reason": "disabled", "matches": []},
    )
    without_semantics = application.build_analysis_result(complete_resume, job_description, "resume.pdf")

    assert baseline["overall_ats_score"] == without_semantics["overall_ats_score"]
    assert baseline["score_breakdown"] == without_semantics["score_breakdown"]
    assert "kubernetes" in baseline["missing_skills"]
    assert "kubernetes" not in {item["value"].casefold() for item in baseline["resume_evidence"]["technologies"]}


def test_requirement_extraction_is_jd_backed_and_keeps_explicit_skills():
    requirements = extract_jd_requirements("Required: Python and Flask. Experience with cloud deployment.")
    values = {item["requirement"].casefold() for item in requirements}

    assert "python" in values
    assert "flask" in values
    assert all(item["source"] == "job_description" for item in requirements)


def test_semantic_labels_use_only_the_dashboard_match_categories():
    class NoMatchModel:
        def encode(self, texts, **_kwargs):
            return np.array([[1.0, 0.0], [0.0, 1.0]], dtype=float)

    assert match_requirements_to_evidence(
        [{"requirement": "unrelated", "source": "job_description", "type": "requirement"}],
        build_resume_evidence("PROJECTS\nPoster: Designed a print layout."),
        model=NoMatchModel(),
    )["matches"][0]["label"] == "No Meaningful Match"
