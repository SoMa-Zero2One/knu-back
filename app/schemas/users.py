from pydantic import BaseModel, Field, ConfigDict

from app.schemas.applications import ApplicationDetail


# Login
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    id: int
    name: str


class UserLoginRequest(BaseModel):
    uuid: str = Field(
        ...,
        description="사용자 고유 UUID",
        example="123e4567-e89b-12d3-a456-426614174000",
    )


# User
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    modify_count: int
    nickname: str
    grade: float
    lang: str
    applications: list[ApplicationDetail] = []


class PublicUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nickname: str
    grade: float
    lang: str
    applications: list[ApplicationDetail] = []


# 지원 대학 수정을 위한 요청의 단일 항목 스키마
class ApplicationChoice(BaseModel):
    university_id: int
    choice: int  # 지망 순위


# 지원 대학 수정 요청 본문 스키마
class UpdateApplicationsRequest(BaseModel):
    applications: list[ApplicationChoice]
