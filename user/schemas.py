from pydantic import BaseModel


class UserSignIn(BaseModel):
    phone: str
    password: str


class UserLogin(UserSignIn):
    pass


# JWT
class TokenSchema(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
