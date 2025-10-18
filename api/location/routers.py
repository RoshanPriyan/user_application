from fastapi import APIRouter
from .views.add_country_api import add_country_api
from .views.get_county_api import country_list_api


router = APIRouter(prefix="/api/v1/location", tags=["Location"])


router.add_api_route("/add-country", add_country_api, methods=["POST"])
router.add_api_route("/list-country", country_list_api, methods=["GET"])
