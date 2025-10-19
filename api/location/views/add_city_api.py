from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from api.location.schemas import AddCitySchema
from api.location.models import StateModel, CityModel
from global_utils import success_response, CustomException, admin_access


async def add_city_api(
        data: AddCitySchema,
        session: Session = Depends(get_db),
        token=Depends(admin_access)
):
    try:
        name = data.name
        state_id = data.state_id

        check_state_exist_stmt = select(StateModel).where(StateModel.id == state_id)
        check_state_exist_exe = session.execute(check_state_exist_stmt)
        state_exist = check_state_exist_exe.scalars().one_or_none()

        if not state_exist:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="state id not found"
            )

        check_city_exit_stmt = select(CityModel).where(CityModel.name == name)
        city_exist = session.execute(check_city_exit_stmt).scalars().one_or_none()

        if city_exist:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"City {city_exist.name} already exist"
            )

        city_data = CityModel(name=name, state_id=state_id)
        session.add(city_data)
        session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            details="City added successfully"
        )

    except SQLAlchemyError as e:
        session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
