from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: str


class UserRoleSchema(BaseModel):
    name: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


class ForgotPasswordSchema(BaseModel):
    email: str
    password: str
    confirm_password: str


class AccountActivateSchema(BaseModel):
    email: str
