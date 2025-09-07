from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: str
