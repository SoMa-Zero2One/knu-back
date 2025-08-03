from pydantic import BaseModel, ConfigDict


class PartnerUniversityInfo(BaseModel):
    id: int
    name: str
    country: str
    slot: int
    applicant_count: int

    model_config = ConfigDict(from_attributes=True)


class ApplicantDetail(BaseModel):
    rank: int
    choice: int
    nickname: str
    grade: float
    lang: str

    model_config = ConfigDict(from_attributes=True)


class UniversityDetailResponse(BaseModel):
    name: str
    country: str
    slot: int
    total_applicants: int
    applicants: list[ApplicantDetail]
