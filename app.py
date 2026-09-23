"""ResumeIQ Flask application and analysis orchestration."""

import os
from datetime import datetime
from io import BytesIO
from xml.etree import ElementTree
from zipfile import ZipFile

from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from xml.sax.saxutils import escape as escape_xml
from werkzeug.utils import secure_filename

from achievement_analyzer import analyze_achievements
from ats_engine import calculate_ats_score
from certification_analyzer import analyze_certifications
from contact_analyzer import analyze_contact
from education_analyzer import analyze_education
from experience_analyzer import analyze_experience
from formatting_analyzer import analyze_formatting
from interview_generator import generate_interview_questions
from interview_coach import build_interview_coach
from language_analyzer import analyze_languages
from project_analyzer import analyze_projects
from resume_advisor import generate_advice
from resume_parser import extract_text
from resume_evidence import build_resume_evidence
from resume_rewriter import rewrite_resume
from score_engine import calculate_weighted_ats_score
from section_detector import detect_resume_sections
from semantic_matcher import extract_jd_requirements, match_requirements_to_evidence
from eligibility_requirements import extract_eligibility_requirements
from career_eligibility import evaluate_career_eligibility


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "Uploaded resume is too large. Please use a file smaller than 16 MB."}), 413


def extract_docx_text(docx_path):
    """Extract paragraph text from a DOCX file using the standard library."""
    with ZipFile(docx_path) as document:
        root = ElementTree.fromstring(document.read("word/document.xml"))

    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    return "\n".join(
        "".join(node.text or "" for node in paragraph.iter(f"{namespace}t"))
        for paragraph in root.iter(f"{namespace}p")
    )


def extract_resume_text(file_path, filename):
    """Use the existing PDF parser or DOCX extraction based on file type."""
    return extract_text(file_path) if filename.lower().endswith(".pdf") else extract_docx_text(file_path)


def build_analysis_result(resume_text, job_description, resume_name):
    """Run each existing analyzer once and assemble one JSON-safe response."""
    contact = analyze_contact(resume_text)
    sections = detect_resume_sections(resume_text)
    education = analyze_education(resume_text)
    experience = analyze_experience(resume_text)
    projects = analyze_projects(resume_text)
    certifications = analyze_certifications(resume_text)
    achievements = analyze_achievements(resume_text)
    languages = analyze_languages(resume_text)
    formatting = analyze_formatting(resume_text)
    resume_evidence = build_resume_evidence(
        resume_text,
        education=education,
        experience=experience,
        projects=projects,
        certifications=certifications,
        achievements=achievements,
        languages=languages,
        contact=contact,
    )

    skills_match = calculate_ats_score(resume_text, job_description)
    ats_result = calculate_weighted_ats_score(
        resume_text,
        job_description,
        skills_match,
        projects,
        experience,
        education,
        sections,
        formatting,
    )
    semantic_result = match_requirements_to_evidence(
        extract_jd_requirements(job_description),
        resume_evidence,
        exact_requirements=ats_result["matched_skills"],
    )
    career_eligibility = evaluate_career_eligibility(extract_eligibility_requirements(job_description), resume_evidence)
    jd_representation = {
        "skills": list(dict.fromkeys([str(item).split(" (", 1)[0] for item in ats_result["matched_skills"] + ats_result["missing_skills"]])),
        "semantic_requirements": extract_jd_requirements(job_description),
        "eligibility_requirements": extract_eligibility_requirements(job_description),
    }

    advice = generate_advice(
        missing_skills=ats_result["missing_skills"],
        formatting_issues=formatting.get("issues", []),
        achievements_info=achievements,
        sections_present=sections,
        matched_skills=ats_result["matched_skills"],
        score_breakdown=ats_result["score_breakdown"],
        resume_evidence=resume_evidence,
        job_description=job_description,
    )
    suggestions = advice["suggestions"]
    for recommendation in advice["recommendations"]:
        if recommendation.get("source") == "job_description":
            recommendation.update({"action_type": "review_skills", "action_target": "skills-section", "action_label": "Review Skills Intelligence"})
        elif recommendation.get("section", "").casefold() in {"formatting", "resume"}:
            recommendation.update({"action_type": "open_rewriter", "action_target": "rewriter-section", "action_label": "Open Resume Rewriter"})
    interview_questions = generate_interview_questions(
        projects,
        experience,
        education,
        ats_result["matched_skills"],
        ats_result["missing_skills"],
        job_description,
        resume_text=resume_text,
        certifications_info=certifications,
        achievements_info=achievements,
        resume_evidence=resume_evidence,
    )
    interview_coach = build_interview_coach(interview_questions, semantic_result, ats_result["matched_skills"], ats_result["missing_skills"])

    return {
        "success": True,
        "resume_name": resume_name,
        "job_description_present": bool(job_description.strip()),
        "resume_text": resume_text,
        "analysis_timestamp": datetime.now().isoformat(),
        "overall_ats_score": ats_result["overall_ats_score"],
        "score_breakdown": ats_result["score_breakdown"],
        "matched_skills": ats_result["matched_skills"],
        "missing_skills": ats_result["missing_skills"],
        "contact": contact,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
        "languages": languages,
        "achievements": achievements,
        "formatting": formatting,
        "resume_evidence": resume_evidence,
        "semantic_matches": semantic_result,
        "career_eligibility": career_eligibility,
        "jd_representation": jd_representation,
        "suggestions": suggestions[:10],
        "recommendation_details": advice["recommendations"][:15],
        "interview_questions": interview_questions[:15],
        "interview_coach": interview_coach,
        "status": ats_result["status"],
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Validate, analyze, and return one complete resume analysis object."""
    if request.method == "GET":
        return redirect(url_for("home"))

    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    resume = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()
    if not resume.filename:
        return jsonify({"error": "No file selected"}), 400
    if not job_description:
        return jsonify({"error": "No job description provided"}), 400

    filename = secure_filename(resume.filename)
    if not filename or not filename.lower().endswith((".pdf", ".docx")):
        return jsonify({"error": "Please upload a PDF or DOCX resume"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    try:
        resume.save(file_path)
        resume_text = extract_resume_text(file_path, filename)
    except Exception:
        app.logger.exception("Resume extraction failed for %s", filename)
        return jsonify({"error": "Could not extract text from the uploaded resume"}), 400
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    if len(resume_text.strip()) < 100:
        return jsonify({"error": "Could not extract enough text from the uploaded resume"}), 400

    try:
        return jsonify(build_analysis_result(resume_text, job_description, filename))
    except Exception:
        app.logger.exception("Resume analysis failed for %s", filename)
        return jsonify({"error": "Resume analysis could not be completed"}), 500


@app.route("/rewrite", methods=["POST"])
def rewrite():
    """Return fact-preserving rewrite suggestions for existing resume text."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    resume_text = data.get("resume_text")
    if not isinstance(resume_text, str) or not resume_text.strip():
        return jsonify({"error": "resume_text is required"}), 400
    if len(resume_text) > 100_000:
        return jsonify({"error": "resume_text is too large"}), 400

    job_description = data.get("job_description", "")
    analysis = data.get("analysis")
    if job_description is None:
        job_description = ""
    if not isinstance(job_description, str):
        return jsonify({"error": "job_description must be a string"}), 400
    if analysis is not None and not isinstance(analysis, dict):
        return jsonify({"error": "analysis must be an object"}), 400

    try:
        return jsonify(rewrite_resume(resume_text, job_description, analysis))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception:
        app.logger.exception("Resume rewriting failed")
        return jsonify({"error": "Resume rewriting could not be completed"}), 500


@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    """Generate a readable PDF report from the browser's analysis payload."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No analysis data provided"}), 400

    report = generate_pdf_report(data)
    filename = f"resume-analysis-{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return send_file(
        report,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )


def _pdf_value(value):
    """Flatten analyzer values into readable, font-safe PDF text."""
    if isinstance(value, dict):
        return "; ".join(
            f"{escape_xml(key.replace('_', ' ').title())}: {_pdf_value(item)}"
            for key, item in value.items()
            if item not in (None, "", [], {})
        )
    if isinstance(value, (list, tuple)):
        return ", ".join(_pdf_value(item) for item in value if item not in (None, ""))
    return escape_xml(str(value).encode("ascii", "replace").decode("ascii"))


def _pdf_fields(**fields):
    """Keep report records user-facing; never render analyzer payload objects."""
    return {label: value for label, value in fields.items() if value not in (None, "", [], {})}


def _pdf_recommendation(item):
    return _pdf_fields(
        Title=item.get("title"),
        Recommendation=item.get("description"),
        Priority=item.get("priority"),
        Evidence=item.get("evidence"),
    )


def _pdf_semantic_match(item):
    return _pdf_fields(
        Requirement=item.get("requirement"),
        Relevance=item.get("label"),
        **{"Resume evidence": item.get("evidence"), "Relevant resume section": item.get("section")},
    )


def _pdf_eligibility_requirement(item):
    return _pdf_fields(
        Requirement=item.get("requirement"),
        Status=item.get("status"),
        Evidence=item.get("resume_evidence"),
        **{"Relevant resume section": item.get("evidence_section")},
        Reason=item.get("reason"),
    )


def _pdf_interview_question(item):
    return _pdf_fields(
        Question=item.get("question"),
        Focus=item.get("category"),
        Evidence=item.get("evidence"),
    )


def _pdf_roadmap_item(item):
    return _pdf_fields(Phase=item.get("title"), **{"Preparation topics": item.get("topics")})


def generate_pdf_report(data):
    """Build a true PDF with the report sections, rather than mislabeled HTML."""
    output = BytesIO()
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Title"], alignment=TA_CENTER,
        textColor=colors.HexColor("#1d4ed8"), spaceAfter=8,
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle", parent=styles["Normal"], alignment=TA_CENTER,
        textColor=colors.HexColor("#475569"), spaceAfter=16,
    )
    heading_style = ParagraphStyle(
        "ReportHeading", parent=styles["Heading2"],
        textColor=colors.HexColor("#1e3a8a"), spaceBefore=12, spaceAfter=6,
    )
    body_style = ParagraphStyle("ReportBody", parent=styles["BodyText"], leading=15, spaceAfter=4)
    story = [
        Paragraph("ResumeIQ Analysis Report", title_style),
        Paragraph(
            f"Resume: {_pdf_value(data.get('resume_name', 'Unknown'))}<br/>"
            f"Analyzed: {_pdf_value(data.get('analysis_timestamp', 'Unknown'))}",
            subtitle_style,
        ),
        Paragraph(
            f"Overall ATS Score: {_pdf_value(data.get('overall_ats_score', 0))}% "
            f"({_pdf_value(data.get('status', 'Unknown'))})", heading_style,
        ),
    ]

    breakdown = data.get("score_breakdown") or {}
    rows = [["Category", "Score"]]
    rows.extend([[key.replace("_score", "").title(), _pdf_value(value)] for key, value in breakdown.items()])
    if len(rows) > 1:
        table = Table(rows, colWidths=[70 * mm, 35 * mm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(table)

    recommendation_details = [
        item for item in data.get("recommendation_details", [])
        if isinstance(item, dict)
    ]
    strengths = [
        _pdf_recommendation(item) for item in recommendation_details
        if item.get("source") == "resume_evidence"
        and item.get("jd_relevance")
        and item.get("evidence")
    ]
    priority_improvements = [
        _pdf_recommendation(item) for item in recommendation_details
        if str(item.get("priority", "")).upper() in {"HIGH", "MEDIUM"}
    ]
    remaining_recommendations = [
        _pdf_recommendation(item) for item in recommendation_details
        if str(item.get("priority", "")).upper() not in {"HIGH", "MEDIUM"}
    ]
    sections = (
        ("Resume Overview", {
            "resume": data.get("resume_name", "Unknown"),
            "status": data.get("status", "Unknown"),
        }),
        ("ATS / JD Match", {
            "overall_score": data.get("overall_ats_score", 0),
            "score_breakdown": data.get("score_breakdown"),
            "matched_skills": data.get("matched_skills"),
            "missing_skills": data.get("missing_skills"),
        }),
        ("Smart Insights", "Evidence-backed strengths and practical improvements for this resume."),
        ("Strengths", strengths),
        ("Priority Improvements", priority_improvements),
        ("Skills Intelligence", {
            "matched": data.get("matched_skills"),
            "missing_jd_skills": data.get("missing_skills"),
        }),
        ("Semantic Job Match (semantic relevance only)", {
            "notice": "Related language is preparation context only and does not create a resume skill.",
            "matches": [_pdf_semantic_match(item) for item in (data.get("semantic_matches") or {}).get("matches", []) if isinstance(item, dict)],
        }),
        ("Career Eligibility", {
            "summary": (
                f"SUPPORTED: {(data.get('career_eligibility') or {}).get('supported_count', 0)}; "
                f"CONFLICT: {(data.get('career_eligibility') or {}).get('conflict_count', 0)}; "
                f"NOT_EVIDENCED: {(data.get('career_eligibility') or {}).get('not_evidenced_count', 0)}. "
                "NOT_EVIDENCED means the resume does not contain enough evidence to determine the requirement."
            ),
            "requirements": [_pdf_eligibility_requirement(item) for item in (data.get("career_eligibility") or {}).get("requirements", []) if isinstance(item, dict)],
        }),
        ("Remaining Recommendations", remaining_recommendations or data.get("suggestions")),
        ("Contact", data.get("contact")),
        ("Education", data.get("education")),
        ("Experience", data.get("experience")),
        ("Projects", data.get("projects")),
        ("Certifications", data.get("certifications")),
        ("Achievements", data.get("achievements")),
        ("Languages", data.get("languages")),
        ("Interview Preparation", [_pdf_interview_question(item) for item in data.get("interview_questions", []) if isinstance(item, dict)]),
        ("Interview Coach Preparation Roadmap", [_pdf_roadmap_item(item) for item in (data.get("interview_coach") or {}).get("roadmap", []) if isinstance(item, dict)]),
        ("Formatting Analysis", data.get("formatting")),
    )
    for title, value in sections:
        story.append(Paragraph(title, heading_style))
        story.append(Paragraph(_pdf_value(value) or "No information detected in this resume.", body_style))

    SimpleDocTemplate(
        output, pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title="ResumeIQ Analysis Report",
    ).build(story)
    output.seek(0)
    return output


@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "ResumeIQ"}), 200


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1", host="0.0.0.0", port=5000)
