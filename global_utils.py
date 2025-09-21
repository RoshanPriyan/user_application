from fastapi import Request, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import engine
from database import get_db
from api.user.models import UserAuthModel


# ✅ Debug: test DB connection (without queries)
def test_connection():
    try:
        with engine.connect() as connection:
            print("✅ Database connection successful")
    except Exception as e:
        print("❌ Database connection failed:", str(e))


def success_response(status_code: str, details: str, data=None):
    response = {"status_code": status_code, "details": details}
    if data:
        response["data"] = data
    return response


class CustomException(Exception):
    def __init__(self, status_code, detail, error=None, trace_back=None):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail
        self.error = error
        self.trace_back = trace_back


def verify_token(
        request: Request,
        session: Session = Depends(get_db)
):
    token = request.headers.get("token")

    if not token:
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Token is header"
        )

    validate_token_stmt = select(UserAuthModel).where(UserAuthModel.access_token == token)
    validate_token = session.execute(validate_token_stmt).scalars().one_or_none()

    if not validate_token:
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token in header"
        )
    return validate_token
