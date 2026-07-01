from firebase_admin import firestore
from datetime import datetime
import streamlit as st

db = firestore.client()


# ======================================
# SAVE INTERVIEW
# ======================================
# ======================================
# CREATE TABLE (Dummy for Firestore)
# ======================================

def create_table():
    pass
def save_interview(
    company,
    role,
    score,
    report
):

    uid = st.session_state.user["localId"]

    db.collection("interviews").add({

        "uid": uid,

        "company": company,

        "role": role,

        "score": score,

        "report": report,

        "created_at": datetime.utcnow()

    })


# ======================================
# GET INTERVIEWS
# ======================================

def get_interviews():

    uid = st.session_state.user["localId"]

    docs = (

        db.collection("interviews")

        .where("uid", "==", uid)

        .order_by("created_at", direction=firestore.Query.DESCENDING)

        .stream()

    )

    rows = []

    for doc in docs:

        data = doc.to_dict()

        created = data.get("created_at")

        if created:
            created = created.strftime("%Y-%m-%d %H:%M:%S")
        else:
            created = ""

        rows.append(

            (

                doc.id,

                data.get("company", ""),

                data.get("role", ""),

                data.get("score", 0),

                created

            )

        )

    return rows


# ======================================
# TOTAL INTERVIEWS
# ======================================

def get_total_interviews():

    return len(get_interviews())


# ======================================
# AVERAGE SCORE
# ======================================

def get_average_score():

    rows = get_interviews()

    if not rows:

        return 0

    scores = [

        row[3]

        for row in rows

    ]

    return round(

        sum(scores) / len(scores),

        2

    )


# ======================================
# BEST SCORE
# ======================================

def get_best_score():

    rows = get_interviews()

    if not rows:

        return 0

    return max(

        row[3]

        for row in rows

    )


# ======================================
# LATEST SCORE
# ======================================

def get_latest_score():

    rows = get_interviews()

    if not rows:

        return 0

    return rows[0][3]
from collections import defaultdict


# ======================================
# DELETE ALL HISTORY
# ======================================

def delete_all_history():

    uid = st.session_state.user["localId"]

    docs = (

        db.collection("interviews")

        .where("uid", "==", uid)

        .stream()

    )

    for doc in docs:

        doc.reference.delete()


# ======================================
# COMPANY PERFORMANCE
# ======================================

def get_company_performance():

    rows = get_interviews()

    company_scores = defaultdict(list)

    for row in rows:

        company = row[1]

        score = row[3]

        company_scores[company].append(score)

    result = []

    for company, scores in company_scores.items():

        avg = round(sum(scores) / len(scores), 2)

        result.append(

            (

                company,

                avg

            )

        )

    return result


# ======================================
# ROLE PERFORMANCE
# ======================================

def get_role_performance():

    rows = get_interviews()

    role_scores = defaultdict(list)

    for row in rows:

        role = row[2]

        score = row[3]

        role_scores[role].append(score)

    result = []

    for role, scores in role_scores.items():

        avg = round(sum(scores) / len(scores), 2)

        result.append(

            (

                role,

                avg

            )

        )

    return result


# ======================================
# DASHBOARD STATS
# ======================================

def get_dashboard_stats():

    return {

        "total": get_total_interviews(),

        "average": get_average_score(),

        "best": get_best_score(),

        "latest": get_latest_score()

    }


# ======================================
# RECENT INTERVIEWS
# ======================================

def get_recent_interviews(limit=5):

    rows = get_interviews()

    recent = []

    for row in rows[:limit]:

        recent.append(

            (

                row[1],

                row[2],

                row[3],

                row[4]

            )

        )

    return recent


# ======================================
# WEEKLY PROGRESS
# ======================================

def get_weekly_progress():

    uid = st.session_state.user["localId"]

    docs = (

        db.collection("interviews")

        .where("uid", "==", uid)

        .stream()

    )

    daily = defaultdict(list)

    for doc in docs:

        data = doc.to_dict()

        created = data.get("created_at")

        score = data.get("score", 0)

        if created:

            day = created.strftime("%Y-%m-%d")

            daily[day].append(score)

    result = []

    for day in sorted(daily.keys()):

        avg = round(

            sum(daily[day]) / len(daily[day]),

            2

        )

        result.append(

            (

                day,

                avg

            )

        )

    return result


# ======================================
# CAREER SCORE
# ======================================

def calculate_career_score():

    stats = get_dashboard_stats()

    total = stats["total"]

    average = stats["average"]

    best = stats["best"]

    score = 0

    score += min(total * 2, 20)

    score += average * 0.6

    score += best * 0.2

    score = min(

        round(score),

        100

    )

    return score