from fastapi import APIRouter
from api.user.views.register_api import user_register_api
from api.user.views.add_roles_api import create_role_api
from api.user.views.login_api import user_login_api


router = APIRouter(prefix="/api/v1/user", tags=["Users"])

router.add_api_route("/register", user_register_api, methods=["POST"])
router.add_api_route("/role", create_role_api, methods=["POST"])
router.add_api_route("/login", user_login_api, methods=["POST"])
