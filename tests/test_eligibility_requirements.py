from eligibility_requirements import extract_eligibility_requirements

def test_extracts_only_explicit_requirements():
    values = extract_eligibility_requirements("B.Tech degree required. Minimum CGPA of 7.0. At least 60% academics. Graduating in 2027. Maximum 1 active backlog. Minimum 2 years experience. AWS certification required. Work authorization required.")
    assert {item["requirement_type"] for item in values} >= {"DEGREE", "MIN_CGPA", "MIN_PERCENTAGE", "GRADUATION_YEAR", "MAX_ACTIVE_BACKLOGS", "MIN_EXPERIENCE", "CERTIFICATION", "WORK_AUTHORIZATION"}

def test_vague_or_malformed_jd_is_safe():
    assert extract_eligibility_requirements("Strong academic background and good communication preferred") == []
    assert extract_eligibility_requirements(None) == []
