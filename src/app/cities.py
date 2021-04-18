from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import List
from pydantic import BaseModel

from app.models import City_Pydantic, CityIn_Pydantic, Cities

router = APIRouter()


@router.post("/", response_model=City_Pydantic, status_code=201)
async def create_city(city: CityIn_Pydantic):
    city.denominazione_comune = city.denominazione_comune.lower()
    city_obj = await Cities.create(**city.dict(exclude_unset=True))
    return await City_Pydantic.from_tortoise_orm(city_obj)


@router.get("/{city_id}/", response_model=City_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def read_city(city_id: int):
    return await City_Pydantic.from_queryset_single(Cities.get(id=city_id))


@router.get("/", response_model=List[City_Pydantic])
async def read_all_cities():
    return await City_Pydantic.from_queryset(Cities.all())


@router.put("/{city_id}/", response_model=City_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_city(city_id: int, city: CityIn_Pydantic):
    city.denominazione_comune = city.denominazione_comune.lower()
    await Cities.filter(id=city_id).update(**city.dict(exclude_unset=True))
    return await City_Pydantic.from_queryset_single(Cities.get(id=city_id))


class Status(BaseModel):
    message: str

@router.delete("/{city_id}/", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_city(city_id: int):
    deleted_count = await Cities.filter(id=city_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"City {city_id} not found")

    return Status(message=f"Deleted city {city_id}")