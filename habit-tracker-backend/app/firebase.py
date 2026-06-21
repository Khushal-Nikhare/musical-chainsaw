import os
import logging

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import auth, credentials

logger = logging.getLogger(__name__)
load_dotenv()

_app = None

import os

FIREBASE_CREDENTIALS_json = os.environ.get('MY_SECRET_JSON')
if FIREBASE_CREDENTIALS_json:
    with open('habit-tracker-firebase-adminsdk-fbsvc.json', 'w') as f:
        f.write(FIREBASE_CREDENTIALS_json)

def init_firebase():
    global _app
    if _app is not None:
        return _app

    credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    if not credentials_path:
        raise RuntimeError("FIREBASE_CREDENTIALS_PATH environment variable is not set")

    if not os.path.exists(credentials_path):
        raise RuntimeError(f"Firebase credentials file not found at: {credentials_path}")

    try:
        cred = credentials.Certificate(credentials_path)
        _app = firebase_admin.initialize_app(cred)
        logger.info("Firebase initialized successfully")
        return _app
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        raise


def verify_firebase_token(id_token: str) -> dict:
    try:
        init_firebase()
        decoded = auth.verify_id_token(id_token)
        logger.info(f"Token verified for user: {decoded.get('uid')}")
        return decoded
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        raise
