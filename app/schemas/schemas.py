from pydantic import BaseModel


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
    status: int  # 0: 미인증, 1: 인증, 2: 성적대기중
    grade: float
    lang: str
    modify_count: int
    created_at: str
    updated_at: str
