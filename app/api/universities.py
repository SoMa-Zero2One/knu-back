from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import User
from app.schemas.universities import (
    ApplicantDetail,
    PartnerUniversityInfo,
    UniversityDetailResponse,
)
from app.services.auth import get_current_user
import app.services.university as university_service

router = APIRouter()


@router.get(
    "/",
    response_model=List[PartnerUniversityInfo],
    tags=["Universities"],
)
def read_universities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # JWT 인증 적용!
):
    """
    인증된 사용자를 위해 모든 파트너 대학교 목록을
    (이름, 국가, 모집인원, 현재 지원자 수)와 함께 반환합니다.
    """
    universities_data = university_service.get_universities_with_applicant_count(db)

    return [
        PartnerUniversityInfo(
            id=uni.id,
            name=uni.name,
            country=uni.country,
            slot=uni.slot,
            applicant_count=uni.applicant_count,
        )
        for uni in universities_data
    ]


@router.get(
    "/{university_id}",
    response_model=UniversityDetailResponse,
)
def read_university_details(
    university_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    특정 학교(university_id)의 상세 정보와
    지원자 목록을 함께 반환합니다.
    """
    university = university_service.get_university(db, university_id=university_id)
    if not university:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="University not found"
        )

    applicants_data = university_service.get_applicants_for_university(
        db, university_id=university_id
    )

    applicant_list = []
    for rank, applicant in enumerate(applicants_data, 1):
        applicant_list.append(
            ApplicantDetail(
                rank=rank,
                choice=applicant.choice,
                nickname=applicant.nickname,
                grade=applicant.grade,
                lang=applicant.lang,
            )
        )

    return UniversityDetailResponse(
        name=university.name,
        country=university.country,
        slot=university.slot,
        total_applicants=len(applicant_list),
        applicants=applicant_list,
    )
