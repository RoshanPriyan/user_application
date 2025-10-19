from fastapi import APIRouter
from .views.add_country_api import add_country_api
from .views.get_country_api import country_list_api
from .views.add_state_api import add_state_api
from .views.get_states_api import state_list_api
from .views.add_city_api import add_city_api
from .views.get_city_api import city_list_api


router = APIRouter(prefix="/api/v1/location", tags=["Location"])


router.add_api_route("/add-country", add_country_api, methods=["POST"])
router.add_api_route("/list-country", country_list_api, methods=["GET"])
router.add_api_route("/add-state", add_state_api, methods=["POST"])
router.add_api_route("/list-state", state_list_api, methods=["GET"])
router.add_api_route("/add-city", add_city_api, methods=["POST"])
router.add_api_route("/list-city", city_list_api, methods=["GET"])
