
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth import create_access_token

load_dotenv()

router = APIRouter(prefix="/auth/google", tags=["Google Authentication"])
bearer = HTTPBearer(auto_error=False)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


@router.get("/client-id")
def get_google_client_id():
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="Google Client ID is not configured in .env"
        )

    return {"client_id": GOOGLE_CLIENT_ID}


@router.post("/login")
def google_login(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="Google Client ID is not configured."
        )

    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Google ID token is required."
        )

    try:
        payload = id_token.verify_oauth2_token(
            credentials.credentials,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Google sign-in could not be verified."
        )

    email = payload.get("email", "").lower()

    if not email or not payload.get("email_verified"):
        raise HTTPException(
            status_code=401,
            detail="Please use a verified Google account."
        )

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email=email,
            hashed_password="GOOGLE_OAUTH_ACCOUNT"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
        "email": user.email,
    }