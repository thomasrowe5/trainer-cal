import base64
import json
import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from google_auth_oauthlib.flow import Flow
from sqlmodel import select

from app.db import get_session
from app.models import User

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/calendar",
]
STATE_COOKIE_NAME = "google_oauth_state"

router = APIRouter(prefix="/auth/google", tags=["auth"])


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{name} is not configured",
        )
    return value


def _build_flow(state: Optional[str] = None) -> Flow:
    client_id = _require_env("GOOGLE_CLIENT_ID")
    client_secret = _require_env("GOOGLE_CLIENT_SECRET")
    redirect_uri = _require_env("GOOGLE_REDIRECT_URI")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        state=state,
    )
    flow.redirect_uri = redirect_uri
    return flow


def _extract_email(id_token: Optional[str]) -> Optional[str]:
    if not id_token:
        return None

    try:
        payload_segment = id_token.split(".")[1]
    except IndexError:
        return None

    padding = "=" * (-len(payload_segment) % 4)
    try:
        decoded_bytes = base64.urlsafe_b64decode(payload_segment + padding)
        payload = json.loads(decoded_bytes.decode("utf-8"))
    except (ValueError, json.JSONDecodeError):
        return None

    return payload.get("email")


@router.get("/login")
def google_login() -> RedirectResponse:
    flow = _build_flow()
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    redirect_response = RedirectResponse(url=authorization_url)
    redirect_uri = _require_env("GOOGLE_REDIRECT_URI")
    redirect_response.set_cookie(
        key=STATE_COOKIE_NAME,
        value=state,
        max_age=600,
        httponly=True,
        secure=redirect_uri.startswith("https://"),
        samesite="lax",
    )
    return redirect_response


@router.get("/callback")
def google_callback(request: Request, code: Optional[str] = None, state: Optional[str] = None) -> JSONResponse:
    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing authorization code")

    if not state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing state parameter")

    stored_state = request.cookies.get(STATE_COOKIE_NAME)
    if not stored_state or stored_state != state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state parameter")

    flow = _build_flow(state=state)
    try:
        flow.fetch_token(code=code)
    except Exception as exc:  # pragma: no cover - surface upstream fetch errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to exchange authorization code: {exc}",
        ) from exc

    credentials = flow.credentials
    refresh_token = credentials.refresh_token
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token not returned by Google"
        )

    email = _extract_email(credentials.id_token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to determine user email")

    with get_session() as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            user = User(email=email, google_refresh_token=refresh_token)
            session.add(user)
        else:
            user.google_refresh_token = refresh_token
        session.commit()

    response = JSONResponse({"status": "connected"})
    response.delete_cookie(STATE_COOKIE_NAME)
    return response
