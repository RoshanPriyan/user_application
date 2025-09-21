from sqlalchemy import select
import hashlib
from datetime import datetime
from api.user.models import UserRolesModel, UserAuthModel, UserModel


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
