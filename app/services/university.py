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
            models.PartnerUniversity.id,
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


def get_applicants_for_university(db: Session, university_id: int):
    """
    특정 학교의 지원자 목록을 학점(grade) 내림차순으로 정렬하여 조회합니다.
    """
    return (
        db.query(
            models.User.nickname,
            models.User.grade,
            models.User.lang,
            models.Application.choice,
        )
        .join(models.Application, models.User.id == models.Application.user_id)
        .filter(models.Application.partner_university_id == university_id)
        .order_by(models.User.grade.desc())  # 학점(grade)으로 내림차순 정렬
        .all()
    )


def get_university(db: Session, university_id: int):
    """
    ID로 특정 학교 정보를 조회합니다.
    """
    return (
        db.query(models.PartnerUniversity)
        .filter(models.PartnerUniversity.id == university_id)
        .first()
    )


def get_applicant_counts_for_universities(
    db: Session, university_ids: list[int]
) -> dict[int, int]:
    """
    주어진 대학 ID 리스트에 대해, 각 대학별 총 지원자 수를 계산합니다.
    결과는 {대학ID: 지원자수} 형태의 딕셔너리로 반환합니다.
    """
    # 만약 조회할 대학 ID가 없으면, 빈 딕셔너리를 즉시 반환합니다.
    if not university_ids:
        return {}

    # SQLAlchemy 쿼리를 사용하여 지원자 수를 계산합니다.
    counts_query = (
        db.query(
            models.Application.partner_university_id,
            func.count(
                models.Application.id
            ),  # 각 그룹의 행 수를 세어 지원자 수를 계산
        )
        .filter(
            models.Application.partner_university_id.in_(university_ids)
        )  # ID 목록에 포함된 대학만 필터링
        .group_by(models.Application.partner_university_id)  # 대학 ID별로 그룹화
        .all()
    )

    # [(대학ID, 지원자수), ...] 형태의 결과를 {대학ID: 지원자수} 딕셔너리로 변환하여 반환
    return {university_id: count for university_id, count in counts_query}
