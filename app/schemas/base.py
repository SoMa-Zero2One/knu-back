from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: bool
    detail: str
