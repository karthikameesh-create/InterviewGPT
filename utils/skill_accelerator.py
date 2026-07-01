import math

from utils.role_skill_analyzer import (

    safe_analyze_role_requirements,

    get_missing_skills

)

from utils.learning_resources import (

    generate_learning_cards

)


# ===================================
# SCORE CALCULATOR
# ===================================

def calculate_scores(

    analysis,

    ats_score=0,

    resume_score=0,

    interview_score=0,

    coding_score=0

):

    required = len(

        analysis.get(

            "required_skills",

            []

        )

    )

    preferred = len(

        analysis.get(

            "preferred_skills",

            []

        )

    )

    matched = len(

        analysis.get(

            "matched_skills",

            []

        )

    )

    missing = len(

        analysis.get(

            "roadmap_priority",

            []

        )

    )

    # -----------------------------
    # Technical Score
    # -----------------------------

    if required == 0:

        technical_score = 100

    else:

        technical_score = round(

            (

                matched /

                required

            ) * 100,

            1

        )

    # -----------------------------
    # Placement Score
    # -----------------------------

    placement_score = round(

        (

            technical_score * 0.60 +

            ats_score * 0.20 +

            interview_score * 0.10 +

            coding_score * 0.10

        ),

        1

    )

    # -----------------------------
    # Learning Progress
    # -----------------------------

    if required + preferred == 0:

        learning_progress = 100

    else:

        completed = matched

        total = required + preferred

        learning_progress = round(

            (

                completed /

                total

            ) * 100,

            1

        )

    # -----------------------------
    # Overall Career Score
    # -----------------------------

    career_score = round(

        (

            resume_score * 0.20 +

            ats_score * 0.20 +

            technical_score * 0.30 +

            interview_score * 0.15 +

            coding_score * 0.15

        ),

        1

    )

    return {

        "resume_score": resume_score,

        "ats_score": ats_score,

        "technical_score": technical_score,

        "placement_score": placement_score,

        "learning_progress": learning_progress,

        "career_score": career_score,

        "matched": matched,

        "required": required,

        "preferred": preferred,

        "missing": missing

    }


# ===================================
# READINESS
# ===================================

def calculate_readiness(

    career_score

):

    if career_score >= 90:

        return "Placement Ready"

    elif career_score >= 75:

        return "Interview Ready"

    elif career_score >= 60:

        return "Needs Improvement"

    elif career_score >= 40:

        return "Learning Stage"

    return "Beginner"


# ===================================
# NEXT STEPS
# ===================================

def generate_next_steps(

    analysis,

    limit=5

):

    steps = []

    missing = analysis.get(

        "roadmap_priority",

        []

    )

    for skill in missing[:limit]:

        if isinstance(

            skill,

            dict

        ):

            name = skill.get(

                "name",

                ""

            )

        else:

            name = str(skill)

        if name:

            steps.append(

                f"Learn {name}"

            )

    steps.append(

        "Complete Mock Interview"

    )

    steps.append(

        "Solve 50 DSA Problems"

    )

    return steps
# ===================================
# SKILL ACCELERATOR
# ===================================

def generate_skill_accelerator(

    company,

    role,

    resume_text,

    ats_score=0,

    resume_score=0,

    interview_score=0,

    coding_score=0,

    job_description=""

):

    # ---------------------------------
    # Analyze Candidate
    # ---------------------------------

    analysis = safe_analyze_role_requirements(

        company=company,

        role=role,

        resume_text=resume_text,

        job_description=job_description

    )

    # ---------------------------------
    # Missing Skills
    # ---------------------------------

    missing_skills = get_missing_skills(

        analysis

    )

    # ---------------------------------
    # Learning Resources
    # ---------------------------------

    learning_cards = generate_learning_cards(

        missing_skills,

        company=company,

        role=role

    )

    # ---------------------------------
    # Calculate Scores
    # ---------------------------------

    scores = calculate_scores(

        analysis,

        ats_score=ats_score,

        resume_score=resume_score,

        interview_score=interview_score,

        coding_score=coding_score

    )

    # ---------------------------------
    # Readiness
    # ---------------------------------

    readiness = calculate_readiness(

        scores["career_score"]

    )

    # ---------------------------------
    # Next Steps
    # ---------------------------------

    next_steps = generate_next_steps(

        analysis

    )

    # ---------------------------------
    # Final Response
    # ---------------------------------

    return {

        "career_score":

            scores["career_score"],

        "resume_score":

            scores["resume_score"],

        "ats_score":

            scores["ats_score"],

        "technical_score":

            scores["technical_score"],

        "placement_score":

            scores["placement_score"],

        "learning_progress":

            scores["learning_progress"],

        "readiness":

            readiness,

        "candidate_skills":

            analysis.get(

                "candidate_skills",

                []

            ),

        "matched_skills":

            analysis.get(

                "matched_skills",

                []

            ),

        "required_skills":

            analysis.get(

                "required_skills",

                []

            ),

        "preferred_skills":

            analysis.get(

                "preferred_skills",

                []

            ),

        "missing_skills":

            analysis.get(

                "roadmap_priority",

                []

            ),

        "tools":

            analysis.get(

                "tools",

                []

            ),

        "certifications":

            analysis.get(

                "certifications",

                []

            ),

        "summary":

            analysis.get(

                "summary",

                ""

            ),

        "learning_cards":

            learning_cards,

        "next_steps":

            next_steps

    }
# ===================================
# CAREER STRENGTHS
# ===================================

def get_strengths(result):

    strengths = []

    for skill in result.get(

        "matched_skills",

        []

    ):

        if isinstance(skill, dict):

            strengths.append(

                skill.get(

                    "name",

                    ""

                )

            )

    return strengths


# ===================================
# CAREER WEAKNESSES
# ===================================

def get_weaknesses(result):

    weaknesses = []

    for skill in result.get(

        "missing_skills",

        []

    ):

        if isinstance(skill, dict):

            weaknesses.append(

                skill.get(

                    "name",

                    ""

                )

            )

        else:

            weaknesses.append(

                str(skill)

            )

    return weaknesses


# ===================================
# DASHBOARD SUMMARY
# ===================================

def get_dashboard_summary(result):

    return {

        "career_score":

            result.get(

                "career_score",

                0

            ),

        "readiness":

            result.get(

                "readiness",

                ""

            ),

        "resume_score":

            result.get(

                "resume_score",

                0

            ),

        "ats_score":

            result.get(

                "ats_score",

                0

            ),

        "technical_score":

            result.get(

                "technical_score",

                0

            ),

        "placement_score":

            result.get(

                "placement_score",

                0

            ),

        "learning_progress":

            result.get(

                "learning_progress",

                0

            ),

        "matched_skills":

            len(

                result.get(

                    "matched_skills",

                    []

                )

            ),

        "missing_skills":

            len(

                result.get(

                    "missing_skills",

                    []

                )

            ),

        "recommended_courses":

            len(

                result.get(

                    "learning_cards",

                    []

                )

            )

    }


# ===================================
# IMPROVEMENT SUGGESTIONS
# ===================================

def get_improvement_suggestions(result):

    suggestions = []

    missing = result.get(

        "missing_skills",

        []

    )

    for skill in missing[:5]:

        if isinstance(skill, dict):

            name = skill.get(

                "name",

                ""

            )

        else:

            name = str(skill)

        if name:

            suggestions.append(

                f"Improve {name}"

            )

    if result.get(

        "ats_score",

        0

    ) < 80:

        suggestions.append(

            "Improve resume ATS compatibility"

        )

    if result.get(

        "technical_score",

        0

    ) < 75:

        suggestions.append(

            "Strengthen technical interview preparation"

        )

    if result.get(

        "placement_score",

        0

    ) < 75:

        suggestions.append(

            "Apply to more companies and practice interviews"

        )

    return suggestions


# ===================================
# COMPLETE CAREER REPORT
# ===================================

def generate_career_report(result):

    return {

        "dashboard":

            get_dashboard_summary(

                result

            ),

        "strengths":

            get_strengths(

                result

            ),

        "weaknesses":

            get_weaknesses(

                result

            ),

        "next_steps":

            result.get(

                "next_steps",

                []

            ),

        "learning_cards":

            result.get(

                "learning_cards",

                []

            ),

        "suggestions":

            get_improvement_suggestions(

                result

            ),

        "summary":

            result.get(

                "summary",

                ""

            )

    }


# ===================================
# DEBUG
# ===================================

if __name__ == "__main__":

    print(

        "Skill Accelerator Module Loaded Successfully."

    )