from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from api.user.schemas import UserLoginSchema
from api.user.models import UserModel, UserAuthModel
from api.user.utils import get_user_role, generate_token
from global_utils import success_response, CustomException


async def user_login_api(
        data: UserLoginSchema,
        session: Session = Depends(get_db)
):
    try:
        stmt = select(UserModel).where(UserModel.username == data.username)
        result = session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not user.verify_password(data.password):
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        role = await get_user_role(user.role_id, session)
        token = generate_token(user.username)

        if user.auth_id:
            user_auth = session.get(UserAuthModel, user.auth_id)
            user_auth.access_token = token
        else:
            user_auth = UserAuthModel(access_token=token)
            session.add(user_auth)
            session.flush()
            user.auth_id = user_auth.id

        session.commit()

        response_data = {
            "id": user.id,
            "username": user.username,
            "email_id": user.email,
            "role": role,
            "access_token": token
        }

        return success_response(
            status_code=status.HTTP_200_OK,
            details="User login successfully",
            data=response_data
        )

    except SQLAlchemyError as e:
        session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )

