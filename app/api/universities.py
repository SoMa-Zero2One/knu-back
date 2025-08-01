from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import User
from app.schemas.universities import ApplicantDetail, PartnerUniversityInfo
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

    # CRUD 함수가 반환한 결과(Row 객체 리스트)를
    # PartnerUniversityInfo 스키마에 맞게 변환합니다.
    return [
        PartnerUniversityInfo(
            name=uni.name,
            country=uni.country,
            slot=uni.slot,
            applicant_count=uni.applicant_count,
        )
        for uni in universities_data
    ]


@router.get("/{university_id}", response_model=List[ApplicantDetail])
def read_university_details(
    university_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    특정 학교(university_id)의 지원자 목록을 순위와 함께 반환합니다.
    - 순위는 학점(grade)을 기준으로 동적으로 매겨집니다.
    """
    # 요청된 ID의 학교가 존재하는지 확인
    university = university_service.get_university(db, university_id=university_id)
    if not university:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="University not found"
        )

    # 해당 학교의 지원자 목록을 학점순으로 가져옴
    applicants_data = university_service.get_applicants_for_university(
        db, university_id=university_id
    )

    # 조회된 데이터를 기반으로 순위를 매겨 응답 목록 생성
    response = []
    for rank, applicant in enumerate(applicants_data, 1):  # rank를 1부터 시작
        response.append(
            ApplicantDetail(
                rank=rank,
                choice=applicant.choice,
                nickname=applicant.nickname,
                grade=applicant.grade,
                lang=applicant.lang,
            )
        )

    return response
