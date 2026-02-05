import firebase_admin
from firebase_admin import credentials
import os
import json
from pathlib import Path

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    try:
        # Method 1: Use environment variable (for production/Railway)
        firebase_creds_json = os.getenv('FIREBASE_CREDENTIALS_JSON')

        if firebase_creds_json:
            # Parse JSON from environment variable
            cred_dict = json.loads(firebase_creds_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully (from environment variable)")
        else:
            # Method 2: Use local file (for development)
            cred_path = os.path.join(Path(__file__).resolve().parent.parent, 'firebase-credentials.json')

            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print("Firebase Admin SDK initialized successfully (from file)")
            else:
                print(f"Warning: Firebase credentials not found")
                print(f"  - Set FIREBASE_CREDENTIALS_JSON environment variable, OR")
                print(f"  - Place firebase-credentials.json at: {cred_path}")
                print("Google authentication will not work without Firebase credentials")
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        print("Google authentication will not work")
