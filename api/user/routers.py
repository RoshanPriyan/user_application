from fastapi import APIRouter
from api.user.views.register_api import user_register_api


router = APIRouter(prefix="/api/v1/user", tags=["Users"])
router.add_api_route("/register", user_register_api, methods=["POST"])
