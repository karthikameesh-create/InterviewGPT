from firebase_admin import firestore
from datetime import datetime

# Firestore Database
db = firestore.client()


# ======================================
# CREATE USER
# ======================================

def create_user(uid, email):

    user_ref = db.collection("users").document(uid)

    if not user_ref.get().exists:

        user_ref.set({

            "email": email,

            "created_at": datetime.utcnow(),

            "last_login": datetime.utcnow(),

            "provider": "email",

            "career_score": 0,

            "interview_score": 0,

            "coding_score": 0,

            "total_interviews": 0,

            "total_applications": 0,

            "profile_completed": False

        })

    else:

        user_ref.update({

            "last_login": datetime.utcnow()

        })


# ======================================
# GET USER
# ======================================

def get_user(uid):

    doc = db.collection("users").document(uid).get()

    if doc.exists:

        return doc.to_dict()

    return None


# ======================================
# UPDATE USER
# ======================================

def update_user(uid, data):

    db.collection("users").document(uid).update(data)


# ======================================
# DELETE USER
# ======================================

def delete_user(uid):

    db.collection("users").document(uid).delete()

from firebase_admin import firestore
from datetime import datetime

db = firestore.client()


# ======================================
# SAVE RESUME
# ======================================

def save_resume(uid, resume_text):

    db.collection("users").document(uid).update({

        "resume_uploaded": True,

        "resume_text": resume_text,

        "last_resume_update": datetime.utcnow()

    })


# ======================================
# LOAD RESUME
# ======================================

def load_resume(uid):

    doc = db.collection("users").document(uid).get()

    if not doc.exists:

        return ""

    data = doc.to_dict()

    return data.get(
        "resume_text",
        ""
    )


# ======================================
# DELETE RESUME
# ======================================

def delete_resume(uid):

    db.collection("users").document(uid).update({

        "resume_uploaded": False,

        "resume_text": ""

    })    