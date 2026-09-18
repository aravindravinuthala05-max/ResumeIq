import pytest

from app import build_analysis_result
from edge_case_fixtures import SCENARIOS


PHASE4_SCENARIOS = [
    "no_job_description",
    "student_resume",
    "experienced_multiple_employers",
    "projects_without_work_experience",
    "work_without_projects",
    "many_matching_jd_skills",
    "many_missing_jd_skills",
    "long_many_sections",
    "numerical_metrics",
    "multiple_dates",
    "multiple_projects_technologies",
    "multiple_employers_roles",
    "certified_candidate",
]


def test_experience_questions_keep_role_and_employer_on_one_source_line():
    case = SCENARIOS["multiple_employers_roles"]
    result = build_analysis_result(case["resume"], case["job_description"], "roles.txt")
    questions = [item for item in result["interview_questions"] if item["category"] == "Experience"]
    evidence = {item for question in questions for item in question["evidence"]}

    assert {"Lead Engineer at Oak Systems", "Software Engineer at Pine Systems", "Analyst at Birch Group"} <= evidence
    assert len(questions) == len({question["question"] for question in questions})
    assert all(question["source"] == "resume" for question in questions)
    assert all(question["fact_safe"] is True for question in questions)


def test_project_questions_keep_project_specific_technologies():
    case = SCENARIOS["multiple_projects_technologies"]
    result = build_analysis_result(case["resume"], case["job_description"], "projects.txt")
    project_questions = [item for item in result["interview_questions"] if item["category"] == "Project"]

    by_project = {question["evidence"][0]: question for question in project_questions}
    assert {"Vision Tool", "Commerce API", "Mobile Client"} <= set(by_project)
    assert {"python", "opencv", "tensorflow"} <= set(by_project["Vision Tool"]["evidence"])
    assert "Java" not in by_project["Vision Tool"]["evidence"]
    assert {"java", "mysql"} <= set(by_project["Commerce API"]["evidence"])
    assert "Python" not in by_project["Commerce API"]["evidence"]


def test_jd_only_skills_produce_gap_questions_not_assumed_experience():
    case = SCENARIOS["many_missing_jd_skills"]
    result = build_analysis_result(case["resume"], case["job_description"], "gaps.txt")
    gaps = [item for item in result["interview_questions"] if item["category"] == "JD gap"]
    missing = {skill.casefold() for skill in result["missing_skills"]}

    assert gaps
    assert all(item["source"] == "job_description" for item in gaps)
    assert all(item["jd_match"] is False and item["fact_safe"] is True for item in gaps)
    assert all(set(map(str.casefold, item["evidence"])) <= missing for item in gaps)
    assert all("not currently reflected" in item["question"] for item in gaps)
    assert not any("experience with" in item["question"].lower() and item["source"] == "resume" for item in gaps)


def test_interview_priority_order_and_metadata_are_stable():
    case = SCENARIOS["student_resume"]
    result = build_analysis_result(case["resume"], case["job_description"], "student.txt")
    questions = result["interview_questions"]

    assert questions == sorted(questions, key=lambda item: item["priority"], reverse=True)
    assert len(questions) == len({item["question"] for item in questions})
    assert all({"question", "category", "source", "evidence", "jd_match", "priority", "fact_safe"} <= set(item) for item in questions)
    assert all(item["fact_safe"] is True for item in questions)


def test_advisor_recommendations_are_safe_prioritized_and_deduplicated():
    case = SCENARIOS["many_missing_jd_skills"]
    result = build_analysis_result(case["resume"], case["job_description"], "gaps.txt")
    recommendations = result["recommendation_details"]
    priority_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

    assert recommendations == sorted(recommendations, key=lambda item: priority_rank[item["priority"]])
    assert len(recommendations) == len({(item["title"], item["section"]) for item in recommendations})
    assert all(item["fact_safe"] is True for item in recommendations)
    assert all({"title", "description", "priority", "section", "source", "evidence", "jd_relevance", "fact_safe"} <= set(item) for item in recommendations)
    missing = {skill.casefold() for skill in result["missing_skills"]}
    for item in recommendations:
        if item["source"] == "job_description":
            assert "not supported" in item["description"]
            assert set(map(str.casefold, item["evidence"])) <= missing


@pytest.mark.parametrize("scenario", PHASE4_SCENARIOS)
def test_phase4_edge_scenarios_produce_safe_dashboard_data(scenario):
    case = SCENARIOS[scenario]
    result = build_analysis_result(case["resume"], case["job_description"], f"{scenario}.txt")

    assert result["success"] is True
    assert isinstance(result["interview_questions"], list)
    assert isinstance(result["recommendation_details"], list)
    assert all(item["fact_safe"] is True for item in result["interview_questions"])
    assert all(item["fact_safe"] is True for item in result["recommendation_details"])
    assert all(item["source"] == "job_description" for item in result["interview_questions"] if item["category"] == "JD gap")
    assert result["job_description_present"] is bool(case["job_description"])
