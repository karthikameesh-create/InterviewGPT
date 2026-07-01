from firebase_admin import firestore
import streamlit as st

db = firestore.client()


# ===================================
# CREATE TABLE (Dummy)
# ===================================

def create_job_table():
    pass


# ===================================
# ADD APPLICATION
# ===================================

def add_application(
    company,
    role,
    status,
    application_date,
    notes
):

    uid = st.session_state.user["localId"]

    db.collection("job_applications").add({

        "uid": uid,

        "company": company,

        "role": role,

        "status": status,

        "application_date": application_date,

        "notes": notes

    })


# ===================================
# GET APPLICATIONS
# ===================================

def get_applications():

    uid = st.session_state.user["localId"]

    docs = (

        db.collection("job_applications")

        .where("uid", "==", uid)

        .stream()

    )

    rows = []

    for doc in docs:

        d = doc.to_dict()

        rows.append(

            (

                doc.id,

                d.get("company", ""),

                d.get("role", ""),

                d.get("status", ""),

                d.get("application_date", ""),

                d.get("notes", "")

            )

        )

    return rows
# ===================================
# UPDATE STATUS
# ===================================

def update_application_status(
    application_id,
    status
):

    db.collection(
        "job_applications"
    ).document(
        application_id
    ).update({

        "status": status

    })


# ===================================
# DELETE APPLICATION
# ===================================

def delete_application(
    application_id
):

    db.collection(
        "job_applications"
    ).document(
        application_id
    ).delete()


# ===================================
# JOB STATS
# ===================================

def get_job_stats():

    uid = st.session_state.user["localId"]

    docs = (

        db.collection("job_applications")

        .where("uid", "==", uid)

        .stream()

    )

    stats = {

        "Interested": 0,

        "Applied": 0,

        "OA": 0,

        "Interview": 0,

        "Offer": 0,

        "Rejected": 0

    }

    for doc in docs:

        data = doc.to_dict()

        status = data.get(
            "status",
            "Interested"
        )

        if status in stats:

            stats[status] += 1

    return stats
from collections import defaultdict


# ===================================
# RECENT APPLICATIONS
# ===================================

def get_recent_applications(limit=5):

    rows = get_applications()

    recent = []

    for row in rows[:limit]:

        recent.append(

            (

                row[1],   # company

                row[2],   # role

                row[3],   # status

                row[4]    # application_date

            )

        )

    return recent


# ===================================
# DASHBOARD JOB STATS
# ===================================

def get_dashboard_job_stats():

    rows = get_applications()

    stats = {

        "total": 0,

        "interested": 0,

        "applied": 0,

        "interviews": 0,

        "offers": 0,

        "rejected": 0,

        "companies": 0,

        "roles": 0

    }

    companies = set()

    roles = set()

    stats["total"] = len(rows)

    for row in rows:

        company = row[1]

        role = row[2]

        status = row[3]

        companies.add(company)

        roles.add(role)

        if status == "Interested":

            stats["interested"] += 1

        elif status == "Applied":

            stats["applied"] += 1

        elif status == "Interview":

            stats["interviews"] += 1

        elif status == "Offer":

            stats["offers"] += 1

        elif status == "Rejected":

            stats["rejected"] += 1

    stats["companies"] = len(companies)

    stats["roles"] = len(roles)

    return stats


# ===================================
# RECENT ACTIVITY
# ===================================

def get_recent_activity(limit=10):

    rows = get_applications()

    activities = []

    for row in rows[:limit]:

        activities.append(

            {

                "title": f"{row[1]} - {row[2]}",

                "status": row[3],

                "date": row[4]

            }

        )

    return activities


# ===================================
# APPLICATION TIMELINE
# ===================================

def get_application_timeline():

    rows = get_applications()

    timeline = defaultdict(int)

    for row in rows:

        timeline[row[4]] += 1

    result = []

    for date in sorted(timeline.keys()):

        result.append(

            (

                date,

                timeline[date]

            )

        )

    return result