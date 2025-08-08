from pydantic import BaseModel


class ApplicationDetail(BaseModel):
    choice: int
    universityId: int
    universityName: str
    country: str
    slot: int
    totalApplicants: int
