from fastapi import FastAPI
from api.user.routers import router
from global_utils import test_connection
from middleware import ExceptionHandlerMiddleware
from background_task.example_tasks import print_message


app = FastAPI()
app.include_router(router)

# middleware handled
app.add_middleware(ExceptionHandlerMiddleware)

test_connection()


@app.get("/test-task")
async def test_task():
    task = print_message.delay("Run from API")
    return {"task_id": task.id}
