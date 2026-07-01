import sqlite3


# ===================================
# CONNECTION
# ===================================

def get_connection():

    return sqlite3.connect(
        "interviewgpt.db",
        check_same_thread=False
    )


# ===================================
# CREATE TABLE
# ===================================

def create_job_table():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS job_applications(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            company TEXT,

            role TEXT,

            status TEXT,

            application_date TEXT,

            notes TEXT
        )
        """
    )

    conn.commit()
    conn.close()


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

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO job_applications(

            company,
            role,
            status,
            application_date,
            notes

        )

        VALUES(?,?,?,?,?)
        """,

        (
            company,
            role,
            status,
            application_date,
            notes
        )
    )

    conn.commit()
    conn.close()


# ===================================
# GET APPLICATIONS
# ===================================

def get_applications():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM job_applications
        ORDER BY id DESC
        """
    )

    rows = cur.fetchall()

    conn.close()

    return rows


# ===================================
# UPDATE STATUS
# ===================================

def update_application_status(

    application_id,
    status
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE job_applications
        SET status=?
        WHERE id=?
        """,

        (
            status,
            application_id
        )
    )

    conn.commit()
    conn.close()


# ===================================
# DELETE APPLICATION
# ===================================

def delete_application(

    application_id
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM job_applications
        WHERE id=?
        """,

        (
            application_id,
        )
    )

    conn.commit()
    conn.close()


# ===================================
# JOB STATS
# ===================================

def get_job_stats():

    conn = get_connection()

    cur = conn.cursor()

    stats = {}

    statuses = [
        "Interested",
        "Applied",
        "OA",
        "Interview",
        "Offer",
        "Rejected"
    ]

    for status in statuses:

        cur.execute(
            """
            SELECT COUNT(*)
            FROM job_applications
            WHERE status=?
            """,

            (
                status,
            )
        )

        stats[status] = cur.fetchone()[0]

    conn.close()

    return stats
# ===================================
# RECENT APPLICATIONS
# ===================================

def get_recent_applications(limit=5):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT

            company,
            role,
            status,
            application_date

        FROM job_applications

        ORDER BY id DESC

        LIMIT ?
        """,

        (limit,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows
# ===================================
# DASHBOARD JOB STATS
# ===================================

def get_dashboard_job_stats():

    conn = get_connection()

    cur = conn.cursor()

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

    # -------------------------------
    # Total Applications
    # -------------------------------

    cur.execute(
        """
        SELECT COUNT(*)
        FROM job_applications
        """
    )

    stats["total"] = cur.fetchone()[0]

    # -------------------------------
    # Status Counts (Single Query)
    # -------------------------------

    cur.execute(
        """
        SELECT status, COUNT(*)
        FROM job_applications
        GROUP BY status
        """
    )

    rows = cur.fetchall()

    for status, count in rows:

        if status == "Interested":
            stats["interested"] = count

        elif status == "Applied":
            stats["applied"] = count

        elif status == "Interview":
            stats["interviews"] = count

        elif status == "Offer":
            stats["offers"] = count

        elif status == "Rejected":
            stats["rejected"] = count

    # -------------------------------
    # Unique Companies
    # -------------------------------

    cur.execute(
        """
        SELECT COUNT(DISTINCT company)
        FROM job_applications
        """
    )

    stats["companies"] = cur.fetchone()[0]

    # -------------------------------
    # Unique Roles
    # -------------------------------

    cur.execute(
        """
        SELECT COUNT(DISTINCT role)
        FROM job_applications
        """
    )

    stats["roles"] = cur.fetchone()[0]

    conn.close()

    return stats
# ===================================
# RECENT ACTIVITY
# ===================================

def get_recent_activity(limit=10):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT

            company,

            role,

            status,

            application_date

        FROM job_applications

        ORDER BY id DESC

        LIMIT ?
        """,

        (limit,)
    )

    rows = cur.fetchall()

    conn.close()

    activities = []

    for row in rows:

        activities.append(

            {

                "title": f"{row[0]} - {row[1]}",

                "status": row[2],

                "date": row[3]

            }

        )

    return activities
# ===================================
# APPLICATION TIMELINE
# ===================================

def get_application_timeline():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT

            application_date,

            COUNT(*)

        FROM job_applications

        GROUP BY application_date

        ORDER BY application_date
        """
    )

    rows = cur.fetchall()

    conn.close()

    return rows