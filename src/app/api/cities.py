from app.api import crud
from app.api.models import CityDB, CitySchema
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()


@router.post("/", response_model=CityDB, status_code=201)
async def create_city(payload: CitySchema):
    city_id = await crud.post(payload)

    response_object = {
        "id": city_id,
        "codice_comune": payload.codice_comune,
        "distretto": payload.distretto,
        "denominazione_comune": payload.denominazione_comune,
        "lat": payload.lat,
        "long": payload.long
    }
    return response_object


@router.get("/{id}/", response_model=CityDB)
async def read_city(id: int):
    city = await crud.get(id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.get("/", response_model=List[CityDB])
async def read_all_cities():
    return await crud.get_all()
