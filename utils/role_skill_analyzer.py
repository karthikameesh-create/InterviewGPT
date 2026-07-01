import os
import json
import re

from dotenv import load_dotenv
import google.generativeai as genai

# ===================================
# GEMINI CONFIGURATION
# ===================================

load_dotenv()

genai.configure(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

model = genai.GenerativeModel(
    "gemini-3.1-flash-lite"
)

# ===================================
# COMMON GEMINI RESPONSE
# ===================================

def generate_response(prompt):

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        print(
            "Gemini Error:",
            e
        )

        return ""


# ===================================
# CLEAN JSON RESPONSE
# ===================================

def clean_json_response(text):

    if not text:

        return "{}"

    text = text.strip()

    text = re.sub(

        r"^```(?:json)?\s*",

        "",

        text,

        flags=re.IGNORECASE

    )

    text = re.sub(

        r"\s*```$",

        "",

        text

    )

    return text.strip()


# ===================================
# DEFAULT RESPONSE
# ===================================

def default_response():

    return {

        "candidate_skills": [],

        "required_skills": [],

        "preferred_skills": [],

        "soft_skills": [],

        "tools": [],

        "certifications": [],

        "roadmap_priority": [],

        "summary": ""

    }


# ===================================
# VALIDATE RESPONSE
# ===================================

def validate_response(data):

    required = {

        "candidate_skills": [],

        "required_skills": [],

        "preferred_skills": [],

        "soft_skills": [],

        "tools": [],

        "certifications": [],

        "roadmap_priority": [],

        "summary": ""

    }

    for key, default in required.items():

        if key not in data:

            data[key] = default

    return data


# ===================================
# IMPORTANCE ORDER
# ===================================

IMPORTANCE_ORDER = {

    "Critical": 4,

    "High": 3,

    "Medium": 2,

    "Low": 1

}


# ===================================
# SORT BY IMPORTANCE
# ===================================

def sort_by_importance(items):

    try:

        return sorted(

            items,

            key=lambda x:

                IMPORTANCE_ORDER.get(

                    x.get(

                        "importance",

                        "Low"

                    ),

                    0

                ),

            reverse=True

        )

    except Exception:

        return items


# ===================================
# REMOVE DUPLICATES
# ===================================

def remove_duplicates(items):

    seen = set()

    cleaned = []

    for item in items:

        if isinstance(

            item,

            dict

        ):

            name = item.get(

                "name",

                ""

            ).strip().lower()

        else:

            name = str(

                item

            ).strip().lower()

        if not name:

            continue

        if name in seen:

            continue

        seen.add(name)

        cleaned.append(item)

    return cleaned
# ===================================
# RESUME SKILL EXTRACTOR
# ===================================

def extract_resume_skills(

    resume_text

):

    prompt = f"""
You are an expert Technical Recruiter.

Your ONLY task is to extract the candidate's skills
from the resume.

Resume

{resume_text}

Rules

1. Extract ONLY skills explicitly mentioned.

2. Do NOT infer missing skills.

3. Do NOT compare with any job role.

4. Do NOT recommend anything.

5. Group similar skills only if they are identical.

6. Remove duplicates.

Return ONLY valid JSON.

Return EXACTLY:

{{
    "candidate_skills":[

        {{
            "name":"",
            "category":"Programming Language"
        }}

    ]
}}
"""

    try:

        text = generate_response(

            prompt

        )

        text = clean_json_response(

            text

        )

        data = json.loads(

            text

        )

        skills = data.get(

            "candidate_skills",

            []

        )

        cleaned = []

        seen = set()

        for skill in skills:

            if not isinstance(

                skill,

                dict

            ):

                continue

            name = skill.get(

                "name",

                ""

            ).strip()

            category = skill.get(

                "category",

                "Other"

            ).strip()

            if not name:

                continue

            key = name.lower()

            if key in seen:

                continue

            seen.add(

                key

            )

            cleaned.append(

                {

                    "name": name,

                    "category": category

                }

            )

        return cleaned

    except Exception as e:

        print(

            "Resume Skill Extraction Error:",

            e

        )

        return []


# ===================================
# GET ONLY SKILL NAMES
# ===================================

def get_resume_skill_names(

    resume_text

):

    skills = extract_resume_skills(

        resume_text

    )

    return [

        skill["name"]

        for skill in skills

    ]


# ===================================
# PRINT RESUME SKILLS (DEBUG)
# ===================================

def print_resume_skills(

    resume_text

):

    skills = extract_resume_skills(

        resume_text

    )

    print("\n========== Resume Skills ==========\n")

    for skill in skills:

        print(

            f"{skill['name']}"

            f" ({skill['category']})"

        )

    print("\n===================================\n")

    return skills
# ===================================
# ROLE REQUIREMENT EXTRACTOR
# ===================================

def analyze_role_requirements(

    company,

    role,

    job_description=""

):

    prompt = f"""
You are a Senior Technical Recruiter and Hiring Manager.

Your ONLY job is to identify the skills required
for this role.

Company

{company}

Role

{role}

Job Description

{job_description}

Rules

1. Ignore the candidate resume completely.

2. If Job Description exists,
use it as the primary source.

3. Otherwise infer the industry-standard
requirements.

4. Do NOT compare with any candidate.

5. Do NOT mention missing skills.

6. Recommend only commonly used tools.

7. Recommend certifications only if
they genuinely add value.

Return ONLY valid JSON.

Return EXACTLY this format.

{{
    "required_skills":[
        {{
            "name":"",
            "importance":"",
            "reason":""
        }}
    ],

    "preferred_skills":[
        {{
            "name":"",
            "importance":"",
            "reason":""
        }}
    ],

    "soft_skills":[
        {{
            "name":"",
            "importance":""
        }}
    ],

    "tools":[
        ""
    ],

    "certifications":[
        {{
            "name":"",
            "reason":""
        }}
    ],

    "summary":""
}}

Importance must be one of:

Critical
High
Medium
Low
"""

    try:

        text = generate_response(

            prompt

        )

        text = clean_json_response(

            text

        )

        data = json.loads(

            text

        )

        data = validate_response(

            data

        )

        data["required_skills"] = sort_by_importance(

            remove_duplicates(

                data.get(

                    "required_skills",

                    []

                )

            )

        )

        data["preferred_skills"] = sort_by_importance(

            remove_duplicates(

                data.get(

                    "preferred_skills",

                    []

                )

            )

        )

        data["soft_skills"] = sort_by_importance(

            remove_duplicates(

                data.get(

                    "soft_skills",

                    []

                )

            )

        )

        data["tools"] = remove_duplicates(

            data.get(

                "tools",

                []

            )

        )

        data["certifications"] = remove_duplicates(

            data.get(

                "certifications",

                []

            )

        )

        return data

    except Exception as e:

        print(

            "Role Requirement Error:",

            e

        )

        response = default_response()

        response["summary"] = (

            "Unable to analyze role requirements."

        )

        return response


# ===================================
# GET REQUIRED SKILL NAMES
# ===================================

def get_required_skill_names(

    result

):

    skills = []

    for item in result.get(

        "required_skills",

        []

    ):

        if isinstance(

            item,

            dict

        ):

            name = item.get(

                "name",

                ""

            ).strip()

            if name:

                skills.append(

                    name

                )

        else:

            skills.append(

                str(item)

            )

    return skills


# ===================================
# GET PREFERRED SKILL NAMES
# ===================================

def get_preferred_skill_names(

    result

):

    skills = []

    for item in result.get(

        "preferred_skills",

        []

    ):

        if isinstance(

            item,

            dict

        ):

            name = item.get(

                "name",

                ""

            ).strip()

            if name:

                skills.append(

                    name

                )

        else:

            skills.append(

                str(item)

            )

    return skills
# ===================================
# PYTHON SKILL GAP ENGINE
# ===================================

def calculate_skill_gap(

    candidate_skills,

    role_analysis

):

    candidate_lookup = {

        skill["name"].strip().lower()

        for skill in candidate_skills

    }

    missing_skills = []

    matched_skills = []

    # -----------------------------
    # REQUIRED SKILLS
    # -----------------------------

    for skill in role_analysis.get(

        "required_skills",

        []

    ):

        name = skill.get(

            "name",

            ""

        ).strip()

        if not name:

            continue

        if name.lower() in candidate_lookup:

            matched_skills.append(

                skill

            )

        else:

            missing_skills.append(

                skill

            )

    # -----------------------------
    # PREFERRED SKILLS
    # -----------------------------

    for skill in role_analysis.get(

        "preferred_skills",

        []

    ):

        name = skill.get(

            "name",

            ""

        ).strip()

        if not name:

            continue

        if name.lower() not in candidate_lookup:

            missing_skills.append(

                skill

            )

    role_analysis["candidate_skills"] = candidate_skills

    role_analysis["matched_skills"] = matched_skills

    role_analysis["roadmap_priority"] = sort_by_importance(

        remove_duplicates(

            missing_skills

        )

    )

    return role_analysis


# ===================================
# SAFE ROLE ANALYZZER
# ===================================

def safe_analyze_role_requirements(

    company,

    role,

    resume_text,

    job_description=""

):

    try:

        # -------------------------
        # STEP 1
        # Extract Resume Skills
        # -------------------------

        candidate_skills = extract_resume_skills(

            resume_text

        )

        # -------------------------
        # STEP 2
        # Extract Role Skills
        # -------------------------

        role_analysis = analyze_role_requirements(

            company,

            role,

            job_description

        )

        # -------------------------
        # STEP 3
        # Python Skill Gap Engine
        # -------------------------

        result = calculate_skill_gap(

            candidate_skills,

            role_analysis

        )

        return result

    except Exception as e:

        print(

            "Role Analyzer Error:",

            e

        )

        response = default_response()

        response["summary"] = (

            "Unable to analyze role."

        )

        return response


# ===================================
# GET MISSING SKILLS
# ===================================

def get_missing_skills(

    result

):

    skills = []

    for item in result.get(

        "roadmap_priority",

        []

    ):

        if isinstance(

            item,

            dict

        ):

            name = item.get(

                "name",

                ""

            ).strip()

            if name:

                skills.append(

                    name

                )

        else:

            skills.append(

                str(item)

            )

    return skills


# ===================================
# TOP PRIORITY SKILLS
# ===================================

def get_top_priority_skills(

    result,

    limit=5

):

    return get_missing_skills(

        result

    )[:limit]


# ===================================
# ROLE SUMMARY
# ===================================

def get_role_summary(

    result

):

    return {

        "candidate_skills": len(

            result.get(

                "candidate_skills",

                []

            )

        ),

        "matched_skills": len(

            result.get(

                "matched_skills",

                []

            )

        ),

        "required": len(

            result.get(

                "required_skills",

                []

            )

        ),

        "preferred": len(

            result.get(

                "preferred_skills",

                []

            )

        ),

        "tools": len(

            result.get(

                "tools",

                []

            )

        ),

        "certifications": len(

            result.get(

                "certifications",

                []

            )

        ),

        "priority_skills": len(

            result.get(

                "roadmap_priority",

                []

            )

        )

    }