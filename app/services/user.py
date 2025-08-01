from sqlalchemy.orm import Session, joinedload

from app.models import models


def get_user_by_uuid(db: Session, *, uuid: str) -> models.User | None:
    """
    UUID를 사용하여 사용자를 조회합니다.
    """
    return db.query(models.User).filter(models.User.uuid == uuid).first()


def get_user_with_applications(db: Session, user_id: int) -> models.User | None:
    """
    ID로 단일 사용자를 조회합니다.
    이때 사용자의 지원 정보(applications)와 각 지원 정보에 연결된
    대학 정보(university)까지 JOIN을 통해 한 번에 불러옵니다.
    """
    return (
        db.query(models.User)
        .options(
            joinedload(models.User.applications).joinedload(
                models.Application.university
            )
        )
        .filter(models.User.id == user_id)
        .first()
    )
