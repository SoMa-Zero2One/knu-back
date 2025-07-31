from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import User
from app.schemas.universities import PartnerUniversityInfo
from app.services.auth import get_current_user
from app.services.university import (
    get_universities_with_applicant_count,
)  # 2단계에서 만든 인증 함수

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
    universities_data = get_universities_with_applicant_count(db)

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
