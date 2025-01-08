from pydantic import BaseModel, EmailStr


class FormData(BaseModel):
    name: str
    email: str
    dateTime: str
    reservationTime: str
    durationTime: int
    station: int

class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str  
