from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.services.user as user_service
import app.schemas.users as user_schemas
from app.models import models
from app.core.database import get_db
from app.services.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=user_schemas.UserResponse)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/me", response_model=user_schemas.UserResponse)
def read_me(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        get_current_user
    ),  # 인증 및 현재 유저 정보 획득
):
    """
    현재 로그인된 사용자의 상세 정보와 지원 목록을 함께 조회합니다.
    """
    # 서비스 함수를 호출할 때 경로에서 받은 user_id 대신 current_user.id를 사용합니다.
    db_user = user_service.get_user_with_applications(db, user_id=current_user.id)

    # 이 경우는 거의 발생하지 않지만, 토큰이 유효한데 DB에 유저가 없는 예외 상황을 방지합니다.
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # DB에서 가져온 `db_user.applications`를 `ApplicationDetail` 스키마 리스트로 변환
    applications_details = [
        user_schemas.ApplicationDetail(
            choice=app.choice,
            university_name=app.university.name,
            country=app.university.country,
            slot=app.university.slot,
        )
        for app in db_user.applications
    ]

    # 최종 UserResponse 객체 생성
    # user_id가 아닌 current_user를 사용하므로 모든 정보가 db_user에 이미 있습니다.
    return user_schemas.UserResponse(
        id=db_user.id,
        email=db_user.email,
        nickname=db_user.nickname,
        grade=db_user.grade,
        lang=db_user.lang,
        modify_count=db_user.modify_count,
        applications=applications_details,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
    )


@router.put("/me/applications", response_model=user_schemas.UserResponse)
def update_my_applications(
    request: user_schemas.UpdateApplicationsRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        user_service.update_user_applications(
            db=db, user=current_user, new_applications=request.applications
        )
        db.commit()

        db_user = user_service.get_user_with_applications(db, user_id=current_user.id)

        applications_details = [
            user_schemas.ApplicationDetail(
                choice=app.choice,
                university_name=app.university.name,
                country=app.university.country,
                slot=app.university.slot,
            )
            for app in db_user.applications
        ]

        return user_schemas.UserResponse(
            id=db_user.id,
            email=db_user.email,
            nickname=db_user.nickname,
            grade=db_user.grade,
            lang=db_user.lang,
            modify_count=db_user.modify_count,
            applications=applications_details,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )
        # --- 여기까지 ---

    except ValueError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating applications.",
        )


@router.get("/{user_id}", response_model=user_schemas.PublicUserResponse)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),  # API 접근 인증용
):
    """
    특정 사용자(user_id)의 공개 프로필과 지원 목록을 조회합니다.
    (이메일, 수정횟수, 생성일 등 민감 정보는 제외됩니다.)
    """
    db_user = user_service.get_user_with_applications(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    applications_details = [
        user_schemas.ApplicationDetail(
            choice=app.choice,
            university_name=app.university.name,
            country=app.university.country,
            slot=app.university.slot,
        )
        for app in db_user.applications
    ]

    return user_schemas.PublicUserResponse(
        id=db_user.id,
        nickname=db_user.nickname,
        grade=db_user.grade,
        lang=db_user.lang,
        applications=applications_details,
    )
