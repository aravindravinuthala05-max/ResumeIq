import json
from app import build_analysis_result
from career_eligibility import evaluate_career_eligibility

def evidence(line="B.Tech in Computer Science, CGPA 7.5, 2027"):
    return {"education":[{"value":"B.TECH","type":"degree","section":"education","source_text":line},{"value":"Computer Science","type":"specialization","section":"education","source_text":line},{"value":"7.5","type":"grade","section":"education","source_text":line}],"certifications":[],"experience":[],"skills":[],"technologies":[]}

def req(kind, value, text="requirement"):
    return {"requirement_type":kind,"original_requirement_text":text,"value":value}

def test_supported_conflict_and_missing_are_distinct():
    result=evaluate_career_eligibility([req("MIN_CGPA",7.0),req("GRADUATION_YEAR",2027),req("DEGREE","btech")],evidence())
    assert [item["status"] for item in result["requirements"]] == ["SUPPORTED","SUPPORTED","SUPPORTED"]
    assert evaluate_career_eligibility([req("MIN_CGPA",8.0)],evidence())["requirements"][0]["status"] == "CONFLICT"
    assert evaluate_career_eligibility([req("MIN_CGPA",7.0)],{})["requirements"][0]["status"] == "NOT_EVIDENCED"

def test_payload_is_safe_and_does_not_change_ats(complete_resume, job_description):
    result=build_analysis_result(complete_resume,job_description,"eligibility.pdf")
    assert "career_eligibility" in result
    assert result["career_eligibility"]["requirements_found"] >= 0
    assert result["overall_ats_score"] == build_analysis_result(complete_resume,job_description,"again.pdf")["overall_ats_score"]
    assert not any(item.get("section")=="education" for item in result["resume_evidence"]["technologies"])
    json.dumps(result["career_eligibility"])
