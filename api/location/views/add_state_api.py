from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from api.location.schemas import AddStateSchema
from api.location.models import CountryModel, StateModel
from global_utils import success_response, CustomException, admin_access


async def add_state_api(
        data: AddStateSchema,
        session: Session = Depends(get_db),
        token=Depends(admin_access)
):
    try:
        name = data.name
        country_id = data.country_id

        check_country_exist_stmt = select(CountryModel).where(CountryModel.id == country_id)
        check_country_exist_exe = session.execute(check_country_exist_stmt)
        check_country_exist = check_country_exist_exe.scalars().one_or_none()

        if not check_country_exist:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Country id not found"
            )

        check_state_exit_stmt = select(StateModel).where(StateModel.name == name)
        state_exist = session.execute(check_state_exit_stmt).scalars().one_or_none()

        if state_exist:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"State {state_exist.name} already exist"
            )

        state_data = StateModel(name=name, country_id=country_id)
        session.add(state_data)
        session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            details="state added successfully"
        )

    except SQLAlchemyError as e:
        session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
