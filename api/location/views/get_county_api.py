from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import traceback
from database import get_db
from api.location.models import CountryModel
from global_utils import success_response, CustomException, verify_token


async def country_list_api(
        session: Session = Depends(get_db),
        token=Depends(verify_token)
):
    try:
        country_stmt = select(CountryModel.id, CountryModel.name, CountryModel.code)
        country_data = session.execute(country_stmt).mappings().all()
        return success_response(
            status_code=status.HTTP_200_OK,
            details="Country added successfully",
            data=country_data
        )

    except SQLAlchemyError as e:
        session.rollback()
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}",
            error=str(e),
            trace_back=traceback.format_exc()
        )
