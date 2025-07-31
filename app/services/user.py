from sqlalchemy.orm import Session

from app.models import models


def get_user_by_uuid(db: Session, *, uuid: str) -> models.User | None:
    """
    UUID를 사용하여 사용자를 조회합니다.
    """
    return db.query(models.User).filter(models.User.uuid == uuid).first()
