from sqlalchemy.orm import Session, joinedload

from app.models import models
import app.schemas.users as user_schemas


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


def update_user_applications(
    db: Session,
    user: models.User,
    new_applications: list[user_schemas.ApplicationChoice],
) -> models.User:
    """
    사용자의 지원 대학 내역을 업데이트합니다.
    1. 수정 횟수 확인
    2. 기존 지원 내역 삭제
    3. 신규 지원 내역 추가
    4. 수정 횟수 차감
    """
    # 1. 수정 횟수가 0 이하이면 ValueError 발생
    if user.modify_count <= 0:
        raise ValueError("No more modifications allowed")

    # 2. 이 사용자의 기존 지원 내역을 모두 삭제
    db.query(models.Application).filter(models.Application.user_id == user.id).delete(
        synchronize_session=False
    )

    # 3. 요청받은 내역으로 새로운 지원 정보 생성
    for app_choice in new_applications:
        db_application = models.Application(
            user_id=user.id,
            partner_university_id=app_choice.university_id,
            choice=app_choice.choice,
        )
        db.add(db_application)

    # 4. 사용자 수정 횟수 1 차감
    user.modify_count -= 1
    db.add(user)

    return user
