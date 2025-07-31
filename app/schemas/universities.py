from pydantic import BaseModel, ConfigDict


class PartnerUniversityInfo(BaseModel):
    name: str
    country: str
    slot: int
    applicant_count: int

    # SQLAlchemy 객체의 속성을 직접 읽어올 수 있도록 설정
    model_config = ConfigDict(from_attributes=True)
