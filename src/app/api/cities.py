from app.api.repositories import city_repository as crud
from app.api.models import CityDB, CitySchema
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()


@router.post("/", response_model=CityDB, status_code=201)
async def create_city(payload: CitySchema):
    payload.denominazione_comune = payload.denominazione_comune.lower()
    city_id = await crud.post(payload)

    if not city_id:
        raise HTTPException(status_code=422, detail="Unable to create the city")

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


@router.put("/{id}/", response_model=CityDB)
async def update_city(id: int, payload: CitySchema):
    city = await crud.get(id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    payload.denominazione_comune = payload.denominazione_comune.lower()
    city_id = await crud.put(id, payload)

    if not city_id:
        raise HTTPException(status_code=422, detail="Unable to update the city")

    response_object = {
        "id": city_id,
        "codice_comune": payload.codice_comune,
        "distretto": payload.distretto,
        "denominazione_comune": payload.denominazione_comune,
        "lat": payload.lat,
        "long": payload.long
    }
    return response_object


@router.delete("/{id}/", response_model=CityDB)
async def delete_city(id: int):
    city = await crud.get(id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    await crud.delete(id)

    return city

