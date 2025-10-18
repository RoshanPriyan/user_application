from pydantic import BaseModel


class AddCountrySchema(BaseModel):
    name: str
    code: str


class AddStateSchema(BaseModel):
    country_id: int
    name: str


class AddCitySchema(BaseModel):
    state_id: int
    name: str
