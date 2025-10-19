from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from api.user.models import UserModel, UserAuthModel, UserProfileModel, UserRolesModel
from global_utils import success_response, CustomException, verify_token


async def get_user_profile_api(
        session: Session = Depends(get_db),
        token_user=Depends(verify_token)
):
    try:
        auth_id = token_user.id

        user_data_stmt = (
            select(
                UserModel.id,
                UserModel.username,
                UserProfileModel.first_name,
                UserProfileModel.last_name,
                UserModel.email,
                UserModel.is_active,
                UserModel.created_at,
                UserProfileModel.phone_number,
                UserProfileModel.address_line1,
                UserProfileModel.address_line2,
                UserProfileModel.city,
                UserProfileModel.state,
                UserProfileModel.postal_code,
                UserProfileModel.country,
                UserProfileModel.profile_picture.label("file_path"),
                UserRolesModel.name.label("role")
            )
            .select_from(UserModel)
            .outerjoin(UserProfileModel)
            .outerjoin(UserAuthModel)
            .outerjoin(UserRolesModel)
            .where(UserAuthModel.id == auth_id)
        )
        user_data_exe = session.execute(user_data_stmt)
        user_data = user_data_exe.mappings().first()

        return success_response(
            status_code=status.HTTP_200_OK,
            details="User profile retrieved successfully",
            data=user_data
        )

    except SQLAlchemyError as e:
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
