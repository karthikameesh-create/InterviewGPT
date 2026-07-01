import requests
from firebase_admin import auth as admin_auth

from utils.firebase_config import FIREBASE_API_KEY

BASE_URL = "https://identitytoolkit.googleapis.com/v1"


# ==========================
# Register User
# ==========================
def register_user(email, password):

    url = f"{BASE_URL}/accounts:signUp?key={FIREBASE_API_KEY}"

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)

    data = response.json()

    if response.status_code == 200:
        return True, "Registration Successful"

    return False, data.get("error", {}).get("message", "Registration Failed")


# ==========================
# Login User
# ==========================
def login_user(email, password):

    url = f"{BASE_URL}/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)

    data = response.json()

    if response.status_code == 200:
        return True, data

    return False, data.get("error", {}).get("message", "Login Failed")


# ==========================
# Password Reset
# ==========================
def reset_password(email):

    url = f"{BASE_URL}/accounts:sendOobCode?key={FIREBASE_API_KEY}"

    payload = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return True, "Password reset email sent."

    data = response.json()

    return False, data.get("error", {}).get("message", "Reset Failed")


# ==========================
# Verify Token
# ==========================
def verify_token(id_token):

    try:
        decoded = admin_auth.verify_id_token(id_token)
        return decoded

    except Exception:
        return None