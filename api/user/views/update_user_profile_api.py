from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from api.user.models import UserModel, UserAuthModel, UserProfileModel
from api.user.schemas import UpdateProfileSchema
from global_utils import success_response, CustomException, verify_token


async def update_user_profile_api(
        data: UpdateProfileSchema,
        session: Session = Depends(get_db),
        token_user=Depends(verify_token)
):
    try:
        auth_id = token_user.id

        user_data_stmt = (
            select(UserModel)
            .select_from(UserModel)
            .outerjoin(UserAuthModel)
            .where(UserAuthModel.id == auth_id)
        )
        user_data_exe = session.execute(user_data_stmt)
        user_data = user_data_exe.scalars().first()

        user_profile_data_stmt = (
            select(UserProfileModel)
            .select_from(UserProfileModel)
            .outerjoin(UserModel)
            .where(UserProfileModel.user_id == user_data.id)
        )
        user_profile_data_exe = session.execute(user_profile_data_stmt)
        user_profile_data = user_profile_data_exe.scalars().first()

        if data.username:
            user_data.username = data.username
        if data.first_name:
            user_profile_data.first_name = data.first_name
        if data.last_name:
            user_profile_data.last_name = data.last_name
        if data.email:
            user_data.email = data.email
        if data.phone_number:
            user_profile_data.phone_number = data.phone_number
        if data.address_line1:
            user_profile_data.address_line1 = data.address_line1
        if data.address_line2:
            user_profile_data.address_line2 = data.address_line2
        if data.city:
            user_profile_data.city = data.city
        if data.state:
            user_profile_data.state = data.state
        if data.postal_code:
            user_profile_data.postal_code = data.postal_code
        if data.country:
            user_profile_data.country = data.country
        session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            details="User profile updated successfully",
        )

    except SQLAlchemyError as e:
        session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
