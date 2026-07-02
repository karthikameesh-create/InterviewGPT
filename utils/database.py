import sqlite3

DB_NAME = "interview_history.db"


def create_table():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interviews (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            company TEXT,

            role TEXT,

            score INTEGER,

            report TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    conn.commit()

    conn.close()


def save_interview(
    company,
    role,
    score,
    report
):
    create_table()

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interviews (

            company,
            role,
            score,
            report

        )

        VALUES (?, ?, ?, ?)
        """,
        (
            company,
            role,
            score,
            report
        )
    )

    conn.commit()

    conn.close()


def get_interviews():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            id,
            company,
            role,
            score,
            created_at

        FROM interviews

        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_total_interviews():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM interviews
        """
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_average_score():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT AVG(score)
        FROM interviews
        """
    )

    result = cursor.fetchone()[0]

    conn.close()

    if result is None:
        return 0

    return round(
        result,
        2
    )


def get_best_score():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MAX(score)
        FROM interviews
        """
    )

    result = cursor.fetchone()[0]

    conn.close()

    if result is None:
        return 0

    return result


def get_latest_score():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT score
        FROM interviews
        ORDER BY id DESC
        LIMIT 1
        """
    )

    result = cursor.fetchone()

    conn.close()

    if result is None:
        return 0

    return result[0]


def delete_all_history():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM interviews
        """
    )

    conn.commit()

    conn.close()


def get_company_performance():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            company,
            AVG(score)

        FROM interviews

        GROUP BY company
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_role_performance():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            role,
            AVG(score)

        FROM interviews

        GROUP BY role
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
# ===================================
# DASHBOARD STATS
# ===================================

def get_dashboard_stats():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    stats = {}

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM interviews
        """
    )

    stats["total"] = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT AVG(score)
        FROM interviews
        """
    )

    avg = cursor.fetchone()[0]

    stats["average"] = round(
        avg,
        2
    ) if avg else 0

    cursor.execute(
        """
        SELECT MAX(score)
        FROM interviews
        """
    )

    best = cursor.fetchone()[0]

    stats["best"] = best if best else 0

    cursor.execute(
        """
        SELECT score
        FROM interviews
        ORDER BY id DESC
        LIMIT 1
        """
    )

    latest = cursor.fetchone()

    stats["latest"] = latest[0] if latest else 0

    conn.close()

    return stats
# ===================================
# RECENT INTERVIEWS
# ===================================

def get_recent_interviews(limit=5):

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            company,

            role,

            score,

            created_at

        FROM interviews

        ORDER BY id DESC

        LIMIT ?
        """,

        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
# ===================================
# WEEKLY PROGRESS
# ===================================

def get_weekly_progress():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            DATE(created_at),

            AVG(score)

        FROM interviews

        GROUP BY DATE(created_at)

        ORDER BY DATE(created_at)
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
# ===================================
# CAREER SCORE
# ===================================

def calculate_career_score():

    stats = get_dashboard_stats()

    total = stats["total"]

    average = stats["average"]

    best = stats["best"]

    score = 0

    score += min(
        total * 2,
        20
    )

    score += average * 0.6

    score += best * 0.2

    score = min(
        round(score),
        100
    )

    return score
# ===================================
# AUTO INITIALIZE DATABASE
# ===================================

create_table()