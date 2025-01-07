from pydantic import BaseModel


class FormData(BaseModel):
    name: str
    email: str
    dateTime: str
    reservationTime: str
    durationTime: int
    station: int
