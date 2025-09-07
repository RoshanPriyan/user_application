from database import engine


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
