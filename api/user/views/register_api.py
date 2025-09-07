from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from api.user.schemas import UserSchema
from api.user.models import UserModel
from global_utils import success_response, CustomException


async def user_register_api(
        data: UserSchema,
        session: Session = Depends(get_db)
):
    try:
        user_name = data.username

        existing_user_stmt = select(UserModel).where(UserModel.username == user_name)
        existing_user_exe = session.execute(existing_user_stmt)
        existing_user = existing_user_exe.scalars().one_or_none()

        if existing_user:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exist"
            )

        if data.confirm_password != data.password:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password and confirm password mismatch"
            )

        user = UserModel(
            username=data.username,
            email=data.email
        )
        user.set_password(data.password)
        session.add(user)
        session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            details="User register successfully"
        )

    except SQLAlchemyError as e:
        session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
