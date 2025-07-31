from datetime import datetime
from pydantic import BaseModel, Field


# Login
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserLoginRequest(BaseModel):
    uuid: str = Field(
        ...,
        description="사용자 고유 UUID",
        example="123e4567-e89b-12d3-a456-426614174000",
    )


# sign up
class UserCreate(BaseModel):
    email: str
    uuid: str
    nickname: str
    grade: float
    lang: str


class UserResponse(BaseModel):
    id: int
    email: str
    uuid: str
    nickname: str
    grade: float
    lang: str
    modify_count: int
    created_at: datetime
    updated_at: datetime
