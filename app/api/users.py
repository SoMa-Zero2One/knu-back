from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.services.user as user_service
import app.schemas.users as user_schemas
from app.models import models
from app.core.database import get_db
from app.services.auth import get_current_user
import app.services.university as university_service

router = APIRouter()


@router.get("/me", response_model=user_schemas.UserResponse)
def read_me(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    현재 로그인된 사용자의 상세 정보와 지원 목록을 함께 조회합니다.
    """
    db_user = user_service.get_user_with_applications(db, user_id=current_user.id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    university_ids = [app.university.id for app in db_user.applications]

    applicant_counts = {}
    if university_ids:
        applicant_counts = university_service.get_applicant_counts_for_universities(
            db, university_ids=university_ids
        )

    applications_details = []
    for app in db_user.applications:
        university_id = app.university.id
        applications_details.append(
            user_schemas.ApplicationDetail(
                choice=app.choice,
                universityId=app.university.id,
                universityName=app.university.name,
                country=app.university.country,
                slot=app.university.slot,
                totalApplicants=applicant_counts.get(university_id, 0),
            )
        )

    return user_schemas.UserResponse(
        id=db_user.id,
        email=db_user.email,
        nickname=db_user.nickname,
        grade=db_user.grade,
        lang=db_user.lang,
        modifyCount=db_user.modify_count,
        applications=applications_details,
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

        university_ids = [app.university.id for app in db_user.applications]

        applicant_counts = {}
        if university_ids:
            applicant_counts = university_service.get_applicant_counts_for_universities(
                db, university_ids=university_ids
            )

        applications_details = []
        for app in db_user.applications:
            university_id = app.university.id
            applications_details.append(
                user_schemas.ApplicationDetail(
                    choice=app.choice,
                    universityName=app.university.name,
                    country=app.university.country,
                    slot=app.university.slot,
                    totalApplicants=applicant_counts.get(university_id, 0),
                )
            )

        return user_schemas.UserResponse(
            id=db_user.id,
            email=db_user.email,
            nickname=db_user.nickname,
            grade=db_user.grade,
            lang=db_user.lang,
            modifyCount=db_user.modify_count,
            applications=applications_details,
            createdAt=db_user.created_at,
            updatedAt=db_user.updated_at,
        )

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

    university_ids = [app.university.id for app in db_user.applications]

    applicant_counts = {}
    if university_ids:
        applicant_counts = university_service.get_applicant_counts_for_universities(
            db, university_ids=university_ids
        )

    applications_details = []
    for app in db_user.applications:
        university_id = app.university.id
        applications_details.append(
            user_schemas.ApplicationDetail(
                choice=app.choice,
                universityId=app.university.id,
                universityName=app.university.name,
                country=app.university.country,
                slot=app.university.slot,
                totalApplicants=applicant_counts.get(university_id, 0),
            )
        )

    return user_schemas.PublicUserResponse(
        id=db_user.id,
        nickname=db_user.nickname,
        grade=db_user.grade,
        lang=db_user.lang,
        applications=applications_details,
    )
