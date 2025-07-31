from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import models


def get_universities_with_applicant_count(db: Session):
    """
    모든 파트너 대학교 목록을 각 학교의 지원자 수와 함께 조회합니다.
    """
    # PartnerUniversity와 Application을 LEFT JOIN하여
    # 학교별로 그룹화하고 지원자(Application.id) 수를 계산합니다.
    result = (
        db.query(
            models.PartnerUniversity.name,
            models.PartnerUniversity.country,
            models.PartnerUniversity.slot,
            func.count(models.Application.id).label("applicant_count"),
        )
        .outerjoin(
            models.Application,
            models.PartnerUniversity.id == models.Application.partner_university_id,
        )
        .group_by(models.PartnerUniversity.id)
        .all()
    )
    return result
