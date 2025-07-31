from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import users
from app.services.user import get_user_by_uuid
from app.services.auth import create_access_token
from app.core.database import get_db  # DB 세션을 가져오는 의존성 함수

router = APIRouter()


@router.post("/token", response_model=users.Token, tags=["Authentication"])
def login_for_access_token(
    login_request: users.UserLoginRequest, db: Session = Depends(get_db)
):
    """
    사용자 UUID를 받아 인증하고 JWT 액세스 토큰을 발급합니다.
    """
    # UUID로 사용자 조회
    user = get_user_by_uuid(db, uuid=login_request.uuid)

    # 사용자가 없으면 404 에러 발생
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with provided UUID not found",
        )

    # JWT 생성 (payload에는 토큰의 주체(subject)를 명시, 보통 user.id나 user.uuid를 사용)
    access_token = create_access_token(
        data={"sub": user.uuid}  # 'sub'은 JWT의 표준 클레임 중 하나입니다.
    )

    return {"access_token": access_token, "token_type": "bearer"}
