import firebase_admin
from firebase_admin import credentials

# Initialize Firebase Admin SDK only once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

# Firebase Web API Key
FIREBASE_API_KEY = "AIzaSyCea-1e3d58-yWPRGKLV_IJxSCzOvvnfRA"