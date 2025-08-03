from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import users as user_schemas
from app.services.user import get_user_by_uuid
from app.services.auth import create_access_token
from app.core.database import get_db

router = APIRouter()


@router.post(
    "/token", response_model=user_schemas.LoginResponse, tags=["Authentication"]
)
def login_for_access_token(
    login_request: user_schemas.UUIDLoginRequest, db: Session = Depends(get_db)
):
    """
    사용자 UUID를 받아 인증하고 JWT와 사용자 정보를 함께 발급합니다.
    """
    user = get_user_by_uuid(db, uuid=login_request.uuid)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with provided UUID not found",
        )

    access_token = create_access_token(data={"sub": user.uuid})

    return {
        "accessToken": access_token,
        "tokenType": "bearer",
        "id": user.id,
        "name": user.nickname,
    }
