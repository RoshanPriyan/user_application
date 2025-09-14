from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from api.user.models import UserRolesModel
from global_utils import success_response, CustomException


async def list_role_api(
        session: Session = Depends(get_db)
):
    try:
        get_role_stmt = select(UserRolesModel.name)
        user_roles_list = session.execute(get_role_stmt).mappings().all()

        return success_response(
            status_code=status.HTTP_200_OK,
            details="Role retrieved successfully",
            data=user_roles_list
        )

    except SQLAlchemyError as e:
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
