from sqlalchemy import select
from api.user.models import UserRolesModel


async def get_role_id(role: str, session):
    get_role_exe = select(UserRolesModel).where(UserRolesModel.name == role)
    role = session.execute(get_role_exe).scalars().one_or_none()
    return role.id


async def get_user_role(role_id: int, session):
    get_role_exe = select(UserRolesModel).where(UserRolesModel.id == role_id)
    role = session.execute(get_role_exe).scalars().one_or_none()
    return role.name
