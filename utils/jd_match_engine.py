import json
import re

from utils.gemini_analyzer import generate_response


# ==========================================
# DEFAULT RESPONSE
# ==========================================

def default_response():

    return {

        "overall_match": 0,

        "recruiter_verdict": "Unknown",

        "interview_probability": 0,

        "skill_match": 0,

        "experience_match": 0,

        "education_match": 0,

        "project_match": 0,

        "keyword_match": 0,

        "matched_skills": [],

        "missing_skills": [],

        "matched_keywords": [],

        "missing_keywords": [],

        "strengths": [],

        "weaknesses": [],

        "resume_improvements": [],

        "resume_rewrite": [],

        "summary": ""

    }


# ==========================================
# CLEAN JSON
# ==========================================

def clean_json(text):

    text = text.strip()

    text = text.replace(

        "```json",

        ""

    )

    text = text.replace(

        "```",

        ""

    )

    start = text.find("{")

    end = text.rfind("}")

    if start == -1 or end == -1:

        return "{}"

    return text[start:end + 1]


# ==========================================
# JD MATCH ANALYSIS
# ==========================================

def analyze_resume_vs_jd(

    resume_text,

    job_description

):

    prompt = f"""

You are a Senior Technical Recruiter.

Compare the resume with the job description.

Return ONLY valid JSON.

Return EXACTLY this schema.

{{
"overall_match":90,
"recruiter_verdict":"Strong Match",
"interview_probability":88,

"skill_match":90,
"experience_match":80,
"education_match":100,
"project_match":85,
"keyword_match":92,

"matched_skills":[
"Python",
"SQL"
],

"missing_skills":[
"Docker",
"Kubernetes"
],

"matched_keywords":[
"REST API",
"Microservices"
],

"missing_keywords":[
"Redis",
"Kafka"
],

"strengths":[
"..."
],

"weaknesses":[
"..."
],

"resume_improvements":[
"..."
],
"summary":"Recruiter executive summary of the candidate in 3-5 sentences.",
"resume_rewrite":[
"..."
],

Resume

{resume_text}

Job Description

{job_description}

"""

    try:

        response = generate_response(

            prompt

        )

        response = clean_json(

            response

        )

        data = json.loads(

            response

        )

        return data

    except Exception:

        return default_response()
# ==========================================
# RECRUITER DECISION
# ==========================================

def recruiter_decision(score):

    if score >= 90:

        return {

            "label": "Strong Match",

            "color": "green",

            "recommendation": "Highly Recommended for Interview"

        }

    elif score >= 75:

        return {

            "label": "Good Match",

            "color": "blue",

            "recommendation": "Recommended for Interview"

        }

    elif score >= 60:

        return {

            "label": "Average Match",

            "color": "orange",

            "recommendation": "Consider After Review"

        }

    else:

        return {

            "label": "Weak Match",

            "color": "red",

            "recommendation": "Not Recommended"

        }


# ==========================================
# SCORE BREAKDOWN
# ==========================================

def build_score_breakdown(result):

    return {

        "Overall Match": result.get(

            "overall_match",

            0

        ),

        "Skill Match": result.get(

            "skill_match",

            0

        ),

        "Experience Match": result.get(

            "experience_match",

            0

        ),

        "Education Match": result.get(

            "education_match",

            0

        ),

        "Project Match": result.get(

            "project_match",

            0

        ),

        "Keyword Match": result.get(

            "keyword_match",

            0

        )

    }


# ==========================================
# MISSING SKILLS
# ==========================================

def get_missing_skills(result):

    return result.get(

        "missing_skills",

        []

    )


# ==========================================
# MATCHED SKILLS
# ==========================================

def get_matched_skills(result):

    return result.get(

        "matched_skills",

        []

    )


# ==========================================
# MISSING KEYWORDS
# ==========================================

def get_missing_keywords(result):

    return result.get(

        "missing_keywords",

        []

    )


# ==========================================
# MATCHED KEYWORDS
# ==========================================

def get_matched_keywords(result):

    return result.get(

        "matched_keywords",

        []

    )


# ==========================================
# STRENGTHS
# ==========================================

def get_strengths(result):

    return result.get(

        "strengths",

        []

    )


# ==========================================
# WEAKNESSES
# ==========================================

def get_weaknesses(result):

    return result.get(

        "weaknesses",

        []

    )


# ==========================================
# RESUME IMPROVEMENTS
# ==========================================

def get_resume_improvements(result):

    return result.get(

        "resume_improvements",

        []

    )


# ==========================================
# RESUME REWRITE
# ==========================================

def get_resume_rewrite(result):

    rewrites = result.get(

        "resume_rewrite",

        []

    )

    if isinstance(rewrites, str):

        rewrites = [

            item.strip()

            for item in rewrites.split(".")

            if item.strip()

        ]

    elif not isinstance(rewrites, list):

        rewrites = []

    return rewrites


# ==========================================
# SUMMARY
# ==========================================

def get_summary(result):

    return result.get(

        "summary",

        ""

    )
# ==========================================
# GENERATE COMPLETE JD REPORT
# ==========================================

def generate_jd_match_report(

    resume_text,

    job_description

):

    result = analyze_resume_vs_jd(

        resume_text,

        job_description

    )

    overall_score = result.get(

        "overall_match",

        0

    )

    report = {

        "overall_match": overall_score,

        "decision": recruiter_decision(

            overall_score

        ),

        "interview_probability": result.get(

            "interview_probability",

            0

        ),

        "score_breakdown": build_score_breakdown(

            result

        ),

        "matched_skills": get_matched_skills(

            result

        ),

        "missing_skills": get_missing_skills(

            result

        ),

        "matched_keywords": get_matched_keywords(

            result

        ),

        "missing_keywords": get_missing_keywords(

            result

        ),

        "strengths": get_strengths(

            result

        ),

        "weaknesses": get_weaknesses(

            result

        ),

        "resume_improvements": get_resume_improvements(

            result

        ),

        "resume_rewrite": get_resume_rewrite(

            result

        ),

        "summary": get_summary(

            result

        )

    }

    return report


# ==========================================
# REPORT VALIDATION
# ==========================================

def validate_report(report):

    if not isinstance(

        report,

        dict

    ):

        return default_response()

    report.setdefault(

        "overall_match",

        0

    )

    report.setdefault(

        "decision",

        recruiter_decision(0)

    )

    report.setdefault(

        "interview_probability",

        0

    )

    report.setdefault(

        "score_breakdown",

        {}

    )

    report.setdefault(

        "matched_skills",

        []

    )

    report.setdefault(

        "missing_skills",

        []

    )

    report.setdefault(

        "matched_keywords",

        []

    )

    report.setdefault(

        "missing_keywords",

        []

    )

    report.setdefault(

        "strengths",

        []

    )

    report.setdefault(

        "weaknesses",

        []

    )

    report.setdefault(

        "resume_improvements",

        []

    )

    report.setdefault(

        "resume_rewrite",

        []

    )

    report.setdefault(

        "summary",

        ""

    )

    return report


# ==========================================
# SAFE WRAPPER
# ==========================================

def safe_generate_jd_match(

    resume_text,

    job_description

):

    try:

        report = generate_jd_match_report(

            resume_text,

            job_description

        )

        return validate_report(

            report

        )

    except Exception:

        return validate_report(

            default_response()

        )
# ==========================================
# SECTION SCORECARD
# ==========================================

def generate_section_scorecard(report):

    score = report.get(
        "overall_match",
        0
    )

    skill_score = report.get(
        "score_breakdown",
        {}
    ).get(
        "Skill Match",
        score
    )

    experience_score = report.get(
        "score_breakdown",
        {}
    ).get(
        "Experience Match",
        score
    )

    education_score = report.get(
        "score_breakdown",
        {}
    ).get(
        "Education Match",
        score
    )

    project_score = report.get(
        "score_breakdown",
        {}
    ).get(
        "Project Match",
        score
    )

    keyword_score = report.get(
        "score_breakdown",
        {}
    ).get(
        "Keyword Match",
        score
    )

    return {

        "Professional Summary": min(
            100,
            keyword_score
        ),

        "Technical Skills": min(
            100,
            skill_score
        ),

        "Projects": min(
            100,
            project_score
        ),

        "Experience": min(
            100,
            experience_score
        ),

        "Education": min(
            100,
            education_score
        )

    }


# ==========================================
# RECRUITER HIGHLIGHTS
# ==========================================

def recruiter_highlights(report):

    strengths = report.get(
        "strengths",
        []
    )

    weaknesses = report.get(
        "weaknesses",
        []
    )

    return {

        "top_strengths": strengths[:5],

        "top_concerns": weaknesses[:5]

    }


# ==========================================
# HIRING STAGE
# ==========================================

def hiring_stage(report):

    score = report.get(
        "overall_match",
        0
    )

    if score >= 95:

        return {

            "stage": "Final Interview",

            "icon": "🏆"

        }

    elif score >= 85:

        return {

            "stage": "Technical Interview",

            "icon": "💻"

        }

    elif score >= 75:

        return {

            "stage": "HR Screening",

            "icon": "👨‍💼"

        }

    elif score >= 60:

        return {

            "stage": "Resume Review",

            "icon": "📄"

        }

    return {

        "stage": "Not Shortlisted",

        "icon": "❌"

    }


# ==========================================
# ANALYSIS CONFIDENCE
# ==========================================

def confidence_score(report):

    overall = report.get(
        "overall_match",
        0
    )

    matched = len(

        report.get(

            "matched_skills",

            []

        )

    )

    missing = len(

        report.get(

            "missing_skills",

            []

        )

    )

    confidence = 50

    confidence += matched * 4

    confidence -= missing * 2

    confidence += overall * 0.25

    confidence = max(

        0,

        min(

            int(confidence),

            100

        )

    )

    return confidence


# ==========================================
# EXECUTIVE DASHBOARD
# ==========================================

def generate_dashboard(report):

    return {

        "section_scores": generate_section_scorecard(

            report

        ),

        "highlights": recruiter_highlights(

            report

        ),

        "confidence": confidence_score(

            report

        ),

        "hiring_stage": hiring_stage(

            report

        )

    }
# ==========================================
# PRIORITIZED IMPROVEMENTS
# ==========================================

def prioritized_improvements(report):

    improvements = report.get(
        "resume_improvements",
        []
    )

    missing_skills = report.get(
        "missing_skills",
        []
    )

    priority = []

    for skill in missing_skills:

        priority.append(

            f"Add or demonstrate experience with {skill}"

        )

    priority.extend(improvements)

    # Remove duplicates while preserving order
    seen = set()
    final = []

    for item in priority:

        if item not in seen:

            seen.add(item)

            final.append(item)

    return final[:10]


# ==========================================
# CRITICAL SKILLS
# ==========================================

def critical_missing_skills(report):

    return report.get(

        "missing_skills",

        []

    )[:5]


# ==========================================
# RECRUITER CHECKLIST
# ==========================================

def recruiter_checklist(report):

    scores = report.get(

        "score_breakdown",

        {}

    )

    return {

        "Skills Match": scores.get(

            "Skill Match",

            0

        ) >= 70,

        "Experience Match": scores.get(

            "Experience Match",

            0

        ) >= 70,

        "Education Match": scores.get(

            "Education Match",

            0

        ) >= 70,

        "Projects Match": scores.get(

            "Project Match",

            0

        ) >= 70,

        "Keyword Match": scores.get(

            "Keyword Match",

            0

        ) >= 70

    }


# ==========================================
# FINAL HIRING SUMMARY
# ==========================================

def final_hiring_summary(report):

    decision = report.get(

        "decision",

        {}

    )

    stage = hiring_stage(report)

    confidence = confidence_score(report)

    return {

        "recommendation": decision.get(

            "recommendation",

            "Unknown"

        ),

        "recruiter_verdict": decision.get(

            "label",

            "Unknown"

        ),

        "expected_stage": stage.get(

            "stage",

            "Unknown"

        ),

        "analysis_confidence": confidence,

        "interview_probability": report.get(

            "interview_probability",

            0

        )

    }


# ==========================================
# EXPORT REPORT
# ==========================================

def export_report(report):

    dashboard = generate_dashboard(report)

    return {

        "summary": report.get(

            "summary",

            ""

        ),

        "overall_match": report.get(

            "overall_match",

            0

        ),

        "decision": report.get(

            "decision",

            {}

        ),

        "score_breakdown": report.get(

            "score_breakdown",

            {}

        ),

        "section_scores": dashboard.get(

            "section_scores",

            {}

        ),

        "matched_skills": report.get(

            "matched_skills",

            []

        ),

        "missing_skills": report.get(

            "missing_skills",

            []

        ),

        "matched_keywords": report.get(

            "matched_keywords",

            []

        ),

        "missing_keywords": report.get(

            "missing_keywords",

            []

        ),

        "strengths": report.get(

            "strengths",

            []

        ),

        "weaknesses": report.get(

            "weaknesses",

            []

        ),

        "resume_improvements": prioritized_improvements(

            report

        ),

        "resume_rewrite": get_resume_rewrite(

        report

        ),

        "dashboard": dashboard,

        "hiring_summary": final_hiring_summary(

            report

        )

    }


# ==========================================
# MAIN ENTRY POINT
# ==========================================

def run_jd_match(

    resume_text,

    job_description

):

    report = safe_generate_jd_match(

        resume_text,

        job_description

    )

    return export_report(

        report

    )        