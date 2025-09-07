from fastapi import FastAPI
from api.user.routers import router
from global_utils import test_connection
from middleware import ExceptionHandlerMiddleware


app = FastAPI()
app.include_router(router)

# middleware handled
app.add_middleware(ExceptionHandlerMiddleware)

test_connection()
