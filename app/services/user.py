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
    """
    # 1-1. 최대 5개 제한 검증
    if len(new_applications) > 5:
        raise ValueError("최대 5개의 지원까지만 가능합니다.")

    # 1-2. choice 순서 검증 (1, 2, 3, 4, 5 순서대로 중간에 빠짐없이)
    if new_applications:
        choices = [app.choice for app in new_applications]
        choices.sort()
        expected_choices = list(range(1, len(new_applications) + 1))

        if choices != expected_choices:
            raise ValueError(
                "choice는 1부터 시작하여 순서대로 중간에 빠짐없이 입력해야 합니다."
            )

    # 1-3. universityId 존재 여부 검증
    from app.services import university as university_service

    for app in new_applications:
        university = university_service.get_university(db, app.universityId)
        if university is None:
            raise ValueError(f"존재하지 않는 대학입니다. (ID: {app.universityId})")

    # 2. 수정 횟수가 0 이하이면 ValueError 발생
    if user.modify_count <= 0:
        raise ValueError("수정 횟수가 부족합니다.")

    # 3. 이 사용자의 기존 지원 내역을 모두 삭제
    db.query(models.Application).filter(models.Application.user_id == user.id).delete(
        synchronize_session=False
    )

    # 4. 요청받은 내역으로 새로운 지원 정보 생성
    for app_choice in new_applications:
        db_application = models.Application(
            user_id=user.id,
            partner_university_id=app_choice.universityId,
            choice=app_choice.choice,
        )
        db.add(db_application)

    # 5. 사용자 수정 횟수 1 차감
    user.modify_count -= 1
    db.add(user)

    return user
