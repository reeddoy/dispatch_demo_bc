import datetime
from fastapi import Depends, HTTPException, Security, Query
from fastapi.security import OAuth2PasswordBearer
import jwt
from starlette.status import *
from fastapi.responses import *

from ....models import *
from .api_models import *

from ..sessions import Session, Sessions
from ....constants.config import SECRET_KEY, SESSION_TIMEOUT, REFRESH_SESSION_TIMEOUT
from ...utils.commons import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


algorithm = "HS256"


def get_access_token(session_id: str, user_id: str, is_admin=False) -> str:
    now = datetime.datetime.utcnow()
    payload = dict(
        session_id=session_id,
        user_id=user_id,
        iat=now,
        is_access=True,
        is_admin=is_admin,
        exp=now + datetime.timedelta(seconds=SESSION_TIMEOUT),
    )
    token = jwt.encode(payload, SECRET_KEY, algorithm=algorithm)
    return token


def get_refresh_token(session_id: str, user_id: str) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = dict(
        session_id=session_id,
        user_id=user_id,
        iat=now,
        is_refresh=True,
        exp=now + datetime.timedelta(days=REFRESH_SESSION_TIMEOUT),
    )
    token = jwt.encode(payload, SECRET_KEY, algorithm=algorithm)
    return token


def _get_session(session_id: str, user_id: str) -> Session:
    session: Session = None

    if session_id and (session := Sessions.get(session_id)):
        session.modified()
    elif user_id:
        if session := Sessions.get_by_user_id(user_id):
            session.modified()
        elif user := Users.get_child(user_id):
            session = Session(user)
            Sessions.add_child(session)

    return session


def token_from_payload(
    token: str = Depends(oauth2_scheme),
    is_refresh=Query(False, include_in_schema=False),
) -> Session:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])
        session_id = payload.get("session_id")
        user_id = payload.get("user_id")

        if is_refresh == True:
            if payload.get("is_refresh"):
                if session := _get_session(session_id, user_id):
                    return session
                else:
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="Invalid Refresh Token: User not found.",
                    )
            else:
                raise HTTPException(
                    status_code=HTTP_406_NOT_ACCEPTABLE,
                    detail="Invalid Refresh Token.",
                )

        elif payload.get("is_access"):
            if session := _get_session(session_id, user_id):
                return session
            else:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Invalid Access Token: User not found.",
                )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Access Token.",
            )
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=f"Expired Access Token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Access Token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


get_session = Security(token_from_payload)
