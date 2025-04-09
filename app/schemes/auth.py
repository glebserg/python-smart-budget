from pydantic import BaseModel, EmailStr


class PostLogin(BaseModel):
    email: EmailStr
    password: str


class PostRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    second_name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str