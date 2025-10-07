from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from api.user.schemas import AccountActivateSchema
from api.user.models import UserModel
from global_utils import success_response, CustomException, verify_token


async def active_user_api(
        data: AccountActivateSchema,
        session: Session = Depends(get_db),
        token=Depends(verify_token)
):
    try:
        email = data.email

        existing_user_stmt = select(UserModel).where(UserModel.email == email)
        existing_user_exe = session.execute(existing_user_stmt)
        existing_user = existing_user_exe.scalars().one_or_none()

        if not existing_user:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User email not registered"
            )

        existing_user.is_active = 1
        session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            details="User activated successfully"
        )

    except SQLAlchemyError as e:
        session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
