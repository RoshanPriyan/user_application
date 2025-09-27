from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from api.user.schemas import ForgotPasswordSchema
from api.user.models import UserModel
from global_utils import success_response, CustomException, verify_token


async def forgot_password_api(
        data: ForgotPasswordSchema,
        session: Session = Depends(get_db),
        token=Depends(verify_token)
):
    try:
        existing_user = select(UserModel).where(UserModel.email == data.email)
        user_details = session.execute(existing_user).scalars().one_or_none()

        if not user_details:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email user not registered"
            )

        if data.confirm_password != data.password:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password and confirm password mismatch"
            )

        user_details.set_password(data.password)
        session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            details="Password updated successfully"
        )

    except SQLAlchemyError as e:
        session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
