from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from api.user.schemas import UserRoleSchema
from api.user.models import UserRolesModel
from global_utils import success_response, CustomException


async def create_role_api(
        data: UserRoleSchema,
        session: Session = Depends(get_db)
):
    try:
        name = data.name.upper()
        if name not in UserRolesModel.roles_list:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role name: {name}. Allowed roles are {UserRolesModel.roles_list}"
            )

        check_stmt = select(UserRolesModel).where(UserRolesModel.name == name)
        existing_role = session.execute(check_stmt).scalars().one_or_none()

        if existing_role:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role '{existing_role.name}' already exist"
            )

        add_role = UserRolesModel(name=name.upper())
        session.add(add_role)
        session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            details="Role added successfully"
        )

    except SQLAlchemyError as e:
        session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
