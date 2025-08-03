from pydantic import BaseModel


class ApplicationDetail(BaseModel):
    choice: int
    university_name: str
    country: str
    slot: int
    total_applicants: int
