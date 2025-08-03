from pydantic import BaseModel, ConfigDict


class PartnerUniversityInfo(BaseModel):
    id: int
    name: str
    country: str
    slot: int
    applicantCount: int

    model_config = ConfigDict(from_attributes=True)


class ApplicantDetail(BaseModel):
    id: int
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
    totalApplicants: int
    applicants: list[ApplicantDetail]
