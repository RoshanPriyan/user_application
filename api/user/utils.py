from fastapi import status
from sqlalchemy import select
import hashlib
from datetime import datetime
from api.user.models import UserRolesModel, UserAuthModel, UserModel
from global_utils import CustomException


async def get_role_id(role: str, session):
    get_role_exe = select(UserRolesModel).where(UserRolesModel.name == role)
    role = session.execute(get_role_exe).scalars().one_or_none()
    return role.id


async def get_user_role(role_id: int, session):
    get_role_exe = select(UserRolesModel).where(UserRolesModel.id == role_id)
    role = session.execute(get_role_exe).scalars().one_or_none()
    return role.name


def generate_token(username: str) -> str:
    data = f"{username}-{datetime.now().isoformat()}"
    token = hashlib.sha256(data.encode()).hexdigest()
    return token


def get_token_user_role(token: str, session):
    get_token_user_stmt = (
        select(UserModel).select_from(UserModel)
        .join(UserModel.auth)
        .where(UserAuthModel.access_token == token)
    )
    get_token_user = session.execute(get_token_user_stmt).scalars().first()
    return get_token_user


async def check_user_active(username: str, session):
    check_user_active_stmt = select(UserModel).where(UserModel.username == username, UserModel.is_active == 1)
    check_user_active_exe = session.execute(check_user_active_stmt)
    active_user = check_user_active_exe.scalar_one_or_none()
    if not active_user:
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive"
        )
