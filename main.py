from fastapi import FastAPI
from api.user.routers import router
from global_utils import test_connection
from middleware import ExceptionHandlerMiddleware
from background_task.example_tasks import print_message
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(router)

origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",
    "http://localhost"
]


# middleware handled
app.add_middleware(ExceptionHandlerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

test_connection()


# @app.get("/test-task")
# async def test_task():
#     task = print_message.delay("Run from API")
#     return {"task_id": task.id}
