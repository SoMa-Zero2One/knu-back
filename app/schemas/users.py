from pydantic import BaseModel, Field, ConfigDict

from app.schemas.applications import ApplicationDetail


# Login
class UUIDLoginRequest(BaseModel):
    uuid: str = Field(
        ...,
        description="사용자 고유 UUID",
        example="123e4567-e89b-12d3-a456-426614174000",
    )


class LoginResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"
    id: int
    nickname: str


# User
class UserResponse(BaseModel):
    id: int
    email: str
    modifyCount: int
    nickname: str
    grade: float
    lang: str
    applications: list[ApplicationDetail] = []

    model_config = ConfigDict(from_attributes=True)


class PublicUserResponse(BaseModel):
    id: int
    nickname: str
    grade: float
    lang: str
    applications: list[ApplicationDetail] = []

    model_config = ConfigDict(from_attributes=True)


# User Application Modify Request
class ApplicationChoice(BaseModel):
    universityId: int
    choice: int


class UpdateApplicationsRequest(BaseModel):
    applications: list[ApplicationChoice]
