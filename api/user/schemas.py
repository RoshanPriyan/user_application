from pydantic import BaseModel
from typing import Optional


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


class UpdateProfileSchema(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    profile_picture: Optional[str] = None
