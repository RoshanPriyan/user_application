from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import traceback
from database import get_db
from api.user.models import UserRolesModel, UserModel
from global_utils import success_response, CustomException, verify_token
from api.user.utils import get_token_user_role, get_user_role


async def user_list_api(
        session: Session = Depends(get_db),
        token=Depends(verify_token)
):
    try:
        user_data = get_token_user_role(token.access_token, session)
        role = await get_user_role(user_data.role_id, session)

        if role != "ADMIN":
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Allowed only 'ADMIN' user"
            )

        all_user_stmt = (
            select(
                UserModel.id,
                UserModel.username,
                UserModel.email,
                UserModel.is_active,
                UserModel.created_at,
                UserRolesModel.name.label("role")
            )
            .select_from(UserModel)
            .join(UserModel.role)
        )
        all_user = session.execute(all_user_stmt).mappings().all()
        for index, data in enumerate(all_user):
            user_dict = dict(data)
            created_at = user_dict.pop("created_at").strftime("%m-%d-%Y %H:%M:%S")
            user_dict["created_date"] = created_at
            all_user[index] = user_dict

        return success_response(
            status_code=status.HTTP_200_OK,
            details="User details retrieved successfully",
            data=all_user
        )

    except SQLAlchemyError as e:
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
