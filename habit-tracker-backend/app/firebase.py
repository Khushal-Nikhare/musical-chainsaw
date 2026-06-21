import os
import logging

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import auth, credentials

logger = logging.getLogger(__name__)
load_dotenv()

_app = None

import os


def init_firebase():
    global _app
    if _app is not None:
        return _app

    # Try to load from env JSON string first
    creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if creds_json:
        try:
            import json
            creds_dict = json.loads(creds_json)
            cred = credentials.Certificate(creds_dict)
            _app = firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized successfully from environment JSON")
            return _app
        except Exception as e:
            logger.error(f"Failed to initialize Firebase from FIREBASE_CREDENTIALS_JSON: {str(e)}")
            raise

    # Fallback to file path
    credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    if not credentials_path:
        raise RuntimeError("Neither FIREBASE_CREDENTIALS_JSON nor FIREBASE_CREDENTIALS_PATH environment variable is set")

    if not os.path.exists(credentials_path):
        raise RuntimeError(f"Firebase credentials file not found at: {credentials_path}")

    try:
        cred = credentials.Certificate(credentials_path)
        _app = firebase_admin.initialize_app(cred)
        logger.info("Firebase initialized successfully from credentials file")
        return _app
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        raise


def verify_firebase_token(id_token: str) -> dict:
    try:
        init_firebase()
        decoded = auth.verify_id_token(id_token, clock_skew_seconds=10)
        logger.info(f"Token verified for user: {decoded.get('uid')}")
        return decoded
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        raise
