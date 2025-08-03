from pydantic import BaseModel


class ApplicationDetail(BaseModel):
    choice: int
    universityName: str
    country: str
    slot: int
    totalApplicants: int
