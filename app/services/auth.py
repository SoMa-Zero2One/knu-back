from datetime import datetime, timedelta, UTC
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from pydantic import BaseModel
from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from jose import JWTError, jwt

from app.services.user import get_user_by_uuid
from app.core.core import SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 35  # 35일


def create_access_token(data: dict) -> str:
    """
    주어진 데이터(payload)를 기반으로 JWT 액세스 토큰을 생성합니다.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class TokenData(BaseModel):
    uuid: str | None = None


api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)


def get_current_user(
    token: str = Depends(api_key_scheme), db: Session = Depends(get_db)
) -> User:
    """
    JWT 토큰을 디코딩하고 검증하여 현재 사용자를 반환합니다.
    이 함수를 Depends()로 사용하면 엔드포인트가 자동으로 보호됩니다.
    """

    scheme, param = get_authorization_scheme_param(token)
    if not token or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(param, SECRET_KEY, algorithms=[ALGORITHM])
        uuid: str | None = payload.get("sub")
        if uuid is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_uuid(db, uuid=uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
