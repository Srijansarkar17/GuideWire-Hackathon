"""
Drizzle — Firebase Admin SDK Initialization
=============================================
Initializes Firebase Admin and exposes a Firestore client singleton.
"""

import logging
import firebase_admin
from firebase_admin import credentials, auth, firestore

from backend.config.settings import FIREBASE_CREDENTIALS_PATH, FIREBASE_PROJECT_ID

log = logging.getLogger("drizzle.firebase")


def _init_firebase() -> firebase_admin.App:
    """Initialize Firebase Admin SDK exactly once."""
    if firebase_admin._apps:
        return firebase_admin.get_app()

    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    app = firebase_admin.initialize_app(cred, {
        "projectId": FIREBASE_PROJECT_ID,
    })
    log.info(f"Firebase Admin initialized — project={FIREBASE_PROJECT_ID}")
    return app


# Initialize on import
_app = _init_firebase()

# Expose singletons
db = firestore.client()


def verify_id_token(id_token: str) -> dict:
    """
    Verify a Firebase ID token from the frontend.
    Returns the decoded token dict with uid, email, etc.
    Raises firebase_admin.auth.InvalidIdTokenError on failure.
    """
    return auth.verify_id_token(id_token)


def get_user(uid: str) -> auth.UserRecord:
    """Fetch a Firebase Auth user record by UID."""
    return auth.get_user(uid)
