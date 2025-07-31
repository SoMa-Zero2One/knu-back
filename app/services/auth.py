from datetime import datetime, timedelta, UTC
from jose import jwt
from pydantic import BaseModel


# 예: from app.core.config import settings
SECRET_KEY = "your-very-secret-key"
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
