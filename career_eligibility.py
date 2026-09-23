"""Evidence-only three-state career and academic requirement comparison."""
from eligibility_requirements import DEGREE_ALIASES, BRANCH_ALIASES

def _records(evidence, group, section=None): return [x for x in (evidence or {}).get(group, []) if isinstance(x, dict) and (section is None or x.get("section") == section)]
def _result(req, status, record=None, reason="Not evidenced in resume"):
    return {"requirement_type": req["requirement_type"], "requirement": req["original_requirement_text"], "status": status, "resume_evidence": record.get("source_text") if record else None, "evidence_section": record.get("section") if record else None, "reason": reason}
def _normal(value, aliases): return aliases.get(str(value).casefold(), str(value).casefold().replace(" ", "_"))
def evaluate_career_eligibility(requirements, resume_evidence):
    results=[]
    for req in requirements or []:
        kind=req.get("requirement_type"); records=[]
        if kind in {"DEGREE","BRANCH","MIN_CGPA","MIN_PERCENTAGE","GRADUATION_YEAR","MAX_ACTIVE_BACKLOGS"}: records=_records(resume_evidence,"education","education")
        elif kind == "CERTIFICATION": records=_records(resume_evidence,"certifications","certifications")
        elif kind == "MIN_EXPERIENCE": records=_records(resume_evidence,"experience","experience")
        elif kind == "WORK_AUTHORIZATION": records=[]
        if not records: results.append(_result(req,"NOT_EVIDENCED")); continue
        record=next((x for x in records if x.get("type") in {"degree","specialization","grade","education_detail","certification","experience_detail"}),records[0]); text=str(record.get("source_text") or record.get("value") or "")
        if kind in {"DEGREE","BRANCH"}:
            aliases=DEGREE_ALIASES if kind=="DEGREE" else BRANCH_ALIASES; actual=_normal(record.get("value"),aliases); expected=req["value"]
            results.append(_result(req,"SUPPORTED" if actual==expected else "CONFLICT",record,"Explicit education evidence matches requirement" if actual==expected else "Explicit education evidence does not match requirement")); continue
        if kind in {"MIN_CGPA","MIN_PERCENTAGE","GRADUATION_YEAR","MAX_ACTIVE_BACKLOGS"}:
            import re; pattern=r"\b\d+(?:\.\d+)?%" if kind=="MIN_PERCENTAGE" else r"\b20\d{2}\b" if kind=="GRADUATION_YEAR" else r"\b(\d+)\s*active backlogs?" if kind=="MAX_ACTIVE_BACKLOGS" else r"\b\d+(?:\.\d+)?\b"; match=re.search(pattern,text)
            if not match: results.append(_result(req,"NOT_EVIDENCED")); continue
            actual=float(match.group().strip("%")); expected=float(req["value"]); supported=actual>=expected if kind in {"MIN_CGPA","MIN_PERCENTAGE"} else actual==expected if kind=="GRADUATION_YEAR" else actual<=expected
            results.append(_result(req,"SUPPORTED" if supported else "CONFLICT",record,"Explicit comparable education evidence satisfies requirement" if supported else "Explicit comparable education evidence conflicts with requirement")); continue
        if kind=="MIN_EXPERIENCE":
            import re; match=re.search(r"\b(\d+(?:\.\d+)?)\s*(years?|months?)\s+(?:of )?experience\b",text,re.I)
            if not match: results.append(_result(req,"NOT_EVIDENCED")); continue
            actual=float(match.group(1)) * (12 if match.group(2).lower().startswith("year") else 1); expected=float(req["value"]) * (12 if req.get("unit","").startswith("year") else 1)
            results.append(_result(req,"SUPPORTED" if actual>=expected else "CONFLICT",record,"Explicit experience duration satisfies requirement" if actual>=expected else "Explicit experience duration conflicts with requirement")); continue
        if kind=="CERTIFICATION":
            expected=req["value"]; supported=expected in text.casefold() or ("aws" in expected and "aws" in text.casefold()); results.append(_result(req,"SUPPORTED" if supported else "NOT_EVIDENCED",record,"Certification evidence satisfies requirement" if supported else "Required certification is not evidenced")); continue
        results.append(_result(req,"NOT_EVIDENCED"))
    counts={s:sum(x["status"]==s for x in results) for s in ("SUPPORTED","CONFLICT","NOT_EVIDENCED")}
    return {"requirements_found":len(results),"supported_count":counts["SUPPORTED"],"conflict_count":counts["CONFLICT"],"not_evidenced_count":counts["NOT_EVIDENCED"],"requirements":results}
