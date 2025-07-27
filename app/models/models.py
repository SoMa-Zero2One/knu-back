from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import UTC, datetime
from app.core.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    uuid = Column(String(36), unique=True, nullable=False)
    nickname = Column(String(255), nullable=False)
    status = Column(
        Integer, default=0, nullable=False
    )  # 0: 미인증, 1: 인증, 2: 성적대기중
    gpa = Column(Float, nullable=False)
    lang = Column(String(255), nullable=False)
    modify_count = Column(Integer, default=3, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC), nullable=False
    )


class PartnerUniversity(Base):
    __tablename__ = "partner_university"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    slot = Column(Integer, nullable=False)
    duration = Column(String(255), nullable=False)  # "1개학기" or "2개학기"
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(UTC), nullable=False)


class Application(Base):
    __tablename__ = "application"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    partner_university_id = Column(
        Integer, ForeignKey("partner_university.id"), nullable=False
    )
    choice = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(UTC), nullable=False)
