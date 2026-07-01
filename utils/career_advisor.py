import json
import re
import os

from dotenv import load_dotenv
import google.generativeai as genai

# ===================================
# GEMINI CONFIGURATION
# ===================================

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-3.1-flash-lite"
)

# ===================================
# COMMON RESPONSE
# ===================================

def generate_response(prompt):

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return str(e)


# ===================================
# CAREER DASHBOARD ADVISOR
# ===================================

def generate_career_advisor(

    career_score,

    ats_score,

    interview_average,

    coding_average,

    total_applications,

    offers,

    resume_summary,

    skill_gap

):

    prompt = f"""
You are a Senior FAANG Career Advisor.

You are preparing a personalized dashboard report.

Career Score

{career_score}/100

ATS Score

{ats_score}/100

Interview Average

{interview_average}/100

Coding Average

{coding_average}/100

Applications

{total_applications}

Offers

{offers}

Resume Summary

{resume_summary}

Skill Gap

{skill_gap}

IMPORTANT

Return ONLY valid JSON.

No markdown.

No explanations.

Format exactly like this:

{{
"readiness":"",

"strengths":[
"",
"",
""
],

"weaknesses":[
"",
"",
""
],

"priority_skills":[
"",
"",
""
],

"recommended_roles":[
"",
"",
""
],

"recommended_companies":[
"",
"",
"",
"",
""
],

"next_steps":[
"",
"",
"",
""
],

"summary":""
}}
"""

    try:

        # -----------------------------
        # Reuse common helper
        # -----------------------------

        text = generate_response(
            prompt
        ).strip()

        # -----------------------------
        # Robust JSON cleanup
        # -----------------------------

        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        ).strip()

        return json.loads(
            text
        )

    except Exception as e:

        # Log for debugging
        print(
            f"Career Advisor Error: {e}"
        )

        return {

            "readiness": "Unknown",

            "strengths": [],

            "weaknesses": [],

            "priority_skills": [],

            "recommended_roles": [],

            "recommended_companies": [],

            "next_steps": [],

            "summary": "Unable to generate career advice at this time. Please try again later."

        }