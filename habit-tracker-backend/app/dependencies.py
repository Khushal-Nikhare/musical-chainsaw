import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.firebase import verify_firebase_token
from app.models.user import User

logger = logging.getLogger(__name__)
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    try:
        decoded = verify_firebase_token(token)
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    firebase_uid = decoded.get("uid")
    if not firebase_uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if user is None:
        user = User(
            firebase_uid=firebase_uid,
            email=decoded.get("email") or "",
            name=decoded.get("name") or decoded.get("email") or "",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user
