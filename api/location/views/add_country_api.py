from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from api.location.schemas import AddCountrySchema
from api.location.models import CountryModel
from global_utils import success_response, CustomException, admin_access


async def add_country_api(
        data: AddCountrySchema,
        session: Session = Depends(get_db),
        token = Depends(admin_access)
):
    try:
        name = data.name.upper()
        code = data.code.upper()

        check_stmt = select(CountryModel).where(CountryModel.name == name)
        existing_country = session.execute(check_stmt).scalars().one_or_none()

        if existing_country:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Country '{existing_country.name}' already exist"
            )

        add_role = CountryModel(name=name, code=code)
        session.add(add_role)
        session.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            details="Country added successfully"
        )

    except SQLAlchemyError as e:
        session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
    