from pydantic import BaseModel


class ScheduleBase(BaseModel):
    md5_hash: str


class Schedule(ScheduleBase):
    id: int

    class Config:
        from_attributes = True


class Email(BaseModel):
    addresses: str
    message: str
    subject: str
