from fastapi import APIRouter
from api.user.views.register_api import user_register_api
from api.user.views.add_roles_api import create_role_api
from api.user.views.login_api import user_login_api
from api.user.views.list_user_roles_api import list_role_api
from api.user.views.user_list_api import user_list_api


router = APIRouter(prefix="/api/v1/user", tags=["Users"])

router.add_api_route("/register", user_register_api, methods=["POST"])
router.add_api_route("/role", create_role_api, methods=["POST"])
router.add_api_route("/login", user_login_api, methods=["POST"])
router.add_api_route("/role-list", list_role_api, methods=["GET"])
router.add_api_route("/user-list", user_list_api, methods=["GET"])
