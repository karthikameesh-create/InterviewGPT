import os
import json
import firebase_admin
import streamlit as st
from firebase_admin import credentials

# =====================================
# FIREBASE INITIALIZATION
# =====================================

if not firebase_admin._apps:

    try:
        # Streamlit Cloud
        firebase_dict = dict(st.secrets["firebase"])

        cred = credentials.Certificate(firebase_dict)

    except Exception:
        # Local Development
        cred = credentials.Certificate("firebase_key.json")

    firebase_admin.initialize_app(cred)

# =====================================
# FIREBASE WEB API KEY
# =====================================

try:
    FIREBASE_API_KEY = st.secrets["FIREBASE_API_KEY"]

except Exception:
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")