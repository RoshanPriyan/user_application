from fastapi import FastAPI
from api.user.routers import router as user_router
from api.location.routers import router as location_router
from global_utils import test_connection
from middleware import ExceptionHandlerMiddleware
from background_task.example_tasks import print_message
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(user_router)
app.include_router(location_router)

# middleware handled
app.add_middleware(ExceptionHandlerMiddleware)
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],  # dev frontends
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

test_connection()


# @app.get("/test-task")
# async def test_task():
#     task = print_message.delay("Run from API")
#     return {"task_id": task.id}
