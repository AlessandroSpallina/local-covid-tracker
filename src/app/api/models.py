# here only the mandatory fields (?)
from pydantic import BaseModel, Field


class CitySchema(BaseModel):
    codice_comune: int
    distretto: int
    denominazione_comune: str = Field(..., min_length=3, max_length=50)
    lat: float
    long: float


class CityDB(CitySchema):
    id: int
