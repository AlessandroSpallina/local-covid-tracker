# here only the mandatory fields (?)
from pydantic import BaseModel


class CitySchema(BaseModel):
    codice_comune: int
    distretto: int
    denominazione_comune: str
    lat: float
    long: float


class CityDB(CitySchema):
    id: int
