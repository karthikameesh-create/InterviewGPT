import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")

URL = "https://jsearch.p.rapidapi.com/search"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}


def search_jobs(
    role,
    location,
    employment_type="",
    page=1
):
    """
    Search live jobs using JSearch API.
    """

    query = role

    if location.strip():
        query += f" in {location}"

    params = {
        "query": query,
        "page": page,
        "num_pages": 1
    }

    try:

        response = requests.get(
            URL,
            headers=HEADERS,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        jobs = []

        for job in data.get("data", []):

            if employment_type:

                emp = (
                    job.get("job_employment_type") or ""
                ).lower()

                if employment_type.lower() not in emp:
                    continue

            jobs.append({

                "company":
                    job.get(
                        "employer_name",
                        "Unknown"
                    ),

                "title":
                    job.get(
                        "job_title",
                        "Unknown"
                    ),

                "location":
                    job.get(
                        "job_city"
                    )
                    or job.get(
                        "job_country"
                    )
                    or "Remote",

                "employment_type":
                    job.get(
                        "job_employment_type",
                        "N/A"
                    ),

                "salary":
                    job.get(
                        "job_salary",
                        "Not Mentioned"
                    ),

                "apply_link":
                    job.get(
                        "job_apply_link",
                        ""
                    ),

                "description":
                    job.get(
                        "job_description",
                        ""
                    )[:400] + "..."

            })

        return jobs

    except Exception as e:

        return {
            "error": str(e)
        }