from fastapi import status
from global_utils import CustomException
from pydantic import BaseModel, field_validator


class UserSchema(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: str
    role: str

    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        roles_list = ["ADMIN", "USER"]
        if value.upper() not in roles_list:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only allowed roles are {roles_list}"
            )
        return value.upper()


class UserRoleSchema(BaseModel):
    name: str


class UserLoginSchema(BaseModel):
    username: str
    password: str
