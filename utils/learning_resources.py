import os
import requests

from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# ==========================================
# CONFIGURATION
# ==========================================
BASE_URL = "https://brave-web-search.p.rapidapi.com/search"

HEADERS = {

    "Content-Type": "application/json",

    "x-rapidapi-key": RAPIDAPI_KEY,

    "x-rapidapi-host": "brave-web-search.p.rapidapi.com"

}
TIMEOUT = 20


# ==========================================
# NORMALIZE SKILL
# ==========================================

def normalize_skill(skill):

    if not skill:
        return ""

    skill = str(skill)

    replacements = {

        "Java or C#/.NET": "Java",

        "C#/.NET": "C#",

        "Cloud Computing (AWS/Azure/GCP)": "AWS",

        "Frontend Frameworks (Angular/React)": "React",

        "Backend Frameworks (Spring Boot/Django/Express)": "Spring Boot",

        "SQL/Relational Databases": "SQL",

        "NoSQL Databases": "MongoDB",

        "Version Control (Git/GitHub)": "Git",

        "Containerization (Docker/Kubernetes)": "Docker",

        "CI/CD": "GitHub Actions",

        "Data Structures and Algorithms": "Data Structures",

        "Object-Oriented Programming": "OOP"

    }

    if skill in replacements:

        return replacements[skill]

    if "(" in skill:

        skill = skill.split("(")[0]

    if " or " in skill:

        skill = skill.split(" or ")[0]

    if "/" in skill:

        skill = skill.split("/")[0]

    return skill.strip()


# ==========================================
# SEARCH
# ==========================================

def brave_search(

    query,

    max_results=5

):

    try:

        response = requests.get(

            BASE_URL,

            headers=HEADERS,

            params={

                "q": query,

                "count": max_results

            },

            timeout=TIMEOUT

        )

        response.raise_for_status()

        data = response.json()
        import streamlit as st

        

        # Brave APIs return different formats
        if "results" in data:

            return data["results"]

        if "web" in data:

            return data["web"].get(

                "results",

                []

            )

        return []

    except Exception:

        return []
    


# ==========================================
# FORMAT RESULTS
# ==========================================

def format_results(results):

    formatted = []

    seen = set()

    for item in results:

        title = item.get(

            "title",

            ""

        )

        url = item.get(

            "link",

            item.get(

                "url",

                ""

            )

        )

        snippet = item.get(

            "snippet",

            item.get(

                "description",

                ""

            )

        )

        if not title or not url:

            continue

        if url in seen:

            continue

        seen.add(url)

        formatted.append(

            {

                "title": title,

                "url": url,

                "snippet": snippet

            }

        )

    return formatted
# ==========================================
# CATEGORY SEARCHES
# ==========================================

def search_documentation(skill):

    return format_results(

        brave_search(

            f"{skill} official documentation",

            3

        )

    )


def search_courses(skill):

    return format_results(

        brave_search(

            f"{skill} free course OR Coursera OR Udemy OR freeCodeCamp",

            3

        )

    )


def search_certifications(skill):

    return format_results(

        brave_search(

            f"{skill} certification",

            3

        )

    )


def search_github(skill):

    return format_results(

        brave_search(

            f"{skill} GitHub repository",

            3

        )

    )


def search_practice(skill):

    return format_results(

        brave_search(

            f"{skill} practice problems tutorial",

            3

        )

    )


def search_youtube(skill):

    return format_results(

        brave_search(

            f"{skill} YouTube tutorial",

            3

        )

    )


def search_other(skill):

    return format_results(

        brave_search(

            f"{skill}",

            3

        )

    )


# ==========================================
# GET ALL RESOURCES
# ==========================================

def get_skill_resources(skill):

    skill = normalize_skill(skill)

    resources = {

        "documentation":

            search_documentation(

                skill

            ),

        "courses":

            search_courses(

                skill

            ),

        "certifications":

            search_certifications(

                skill

            ),

        "practice":

            search_practice(

                skill

            ),

        "github":

            search_github(

                skill

            ),

        "youtube":

            search_youtube(

                skill

            ),

        "others":

            search_other(

                skill

            )

    }

    return resources


# ==========================================
# TOTAL RESOURCE COUNT
# ==========================================

def total_resources(resources):

    total = 0

    for value in resources.values():

        total += len(value)

    return total
# ==========================================
# GENERATE LEARNING CARDS
# ==========================================

def generate_learning_cards(

    missing_skills,

    company="",

    role=""

):

    learning_cards = []

    if not missing_skills:

        return learning_cards

    seen = set()

    for skill in missing_skills:

        # -----------------------------
        # Handle Dict or String
        # -----------------------------

        if isinstance(skill, dict):

            skill_name = skill.get(

                "name",

                ""

            )

        else:

            skill_name = str(skill)

        skill_name = normalize_skill(

            skill_name

        )

        if not skill_name:

            continue

        key = skill_name.lower()

        if key in seen:

            continue

        seen.add(key)

        # -----------------------------
        # Search Resources
        # -----------------------------

        resources = get_skill_resources(

            skill_name

        )

        learning_cards.append(

            {

                "skill": skill_name,

                "company": company,

                "role": role,

                "total_resources": total_resources(

                    resources

                ),

                "resources": resources

            }

        )

    return learning_cards


# ==========================================
# GET BEST RESOURCE
# ==========================================

def get_best_resource(

    resources,

    category

):

    items = resources.get(

        category,

        []

    )

    if items:

        return items[0]

    return None


# ==========================================
# GET QUICK LINKS
# ==========================================

def get_quick_links(

    learning_cards

):

    quick_links = []

    for card in learning_cards:

        skill = card.get(

            "skill",

            ""

        )

        resources = card.get(

            "resources",

            {}

        )

        for category in [

            "documentation",

            "courses",

            "certifications",

            "practice",

            "github",

            "youtube"

        ]:

            best = get_best_resource(

                resources,

                category

            )

            if best:

                quick_links.append(

                    {

                        "skill": skill,

                        "category": category,

                        "title": best.get(

                            "title",

                            ""

                        ),

                        "url": best.get(

                            "url",

                            ""

                        )

                    }

                )

    return quick_links


# ==========================================
# DEBUG
# ==========================================

if __name__ == "__main__":

    skills = [

        "Docker",

        "AWS",

        "React"

    ]

    cards = generate_learning_cards(

        skills

    )

    from pprint import pprint

    pprint(cards)