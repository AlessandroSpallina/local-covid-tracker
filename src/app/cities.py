from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import List
from pydantic import BaseModel
from uuid import UUID

from app.models import (
    City_Pydantic, CityIn_Pydantic, Cities,
    TrackedDay_Pydantic, TrackedDayIn_Pydantic, TrackedDays
)

router = APIRouter()


class Status(BaseModel):
    message: str


@router.post("/", response_model=City_Pydantic, status_code=201)
async def create_city(city: CityIn_Pydantic):
    city.denominazione_comune = city.denominazione_comune.lower()
    city_obj = await Cities.create(**city.dict(exclude_unset=True))
    return await City_Pydantic.from_tortoise_orm(city_obj)


@router.get("/{city_id}/", response_model=City_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def read_city(city_id: UUID):
    return await City_Pydantic.from_queryset_single(Cities.get(id=city_id))


@router.get("/", response_model=List[City_Pydantic])
async def read_all_cities():
    return await City_Pydantic.from_queryset(Cities.all())


@router.put("/{city_id}/", response_model=City_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_city(city_id: UUID, city: CityIn_Pydantic):
    city.denominazione_comune = city.denominazione_comune.lower()
    await Cities.filter(id=city_id).update(**city.dict(exclude_unset=True))
    return await City_Pydantic.from_queryset_single(Cities.get(id=city_id))


@router.delete("/{city_id}/", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_city(city_id: UUID):
    deleted_count = await Cities.filter(id=city_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"City {city_id} not found")

    return Status(message=f"Deleted City {city_id}")


# --------- Tracked Days ----------

@router.post("/{city_id}/days/", response_model=TrackedDay_Pydantic, status_code=201)
async def create_tracked_day(city_id: UUID, day: TrackedDayIn_Pydantic):
    # operations on data
    day_obj = await TrackedDays.create(**day.dict(exclude_unset=True), city_id=city_id)
    return await TrackedDay_Pydantic.from_tortoise_orm(day_obj)


@router.get("/{city_id}/days/{day_id}/", response_model=TrackedDay_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def read_tracked_day(city_id: UUID, day_id: UUID):
    return await TrackedDay_Pydantic.from_queryset_single(TrackedDays.get(id=day_id, city_id=city_id))


@router.get("/{city_id}/days/", response_model=List[TrackedDay_Pydantic])
async def read_all_tracked_days(city_id: UUID):
    return await TrackedDay_Pydantic.from_queryset(TrackedDays.filter(city_id=city_id).all())


@router.put("/{city_id}/days/{day_id}/", response_model=TrackedDay_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_tracked_day(city_id: UUID, day_id: UUID, day: TrackedDayIn_Pydantic):
    # operations on data
    await TrackedDays.filter(id=day_id, city_id=city_id).update(**day.dict(exclude_unset=True))
    return await TrackedDay_Pydantic.from_queryset_single(TrackedDays.get(id=day_id, city_id=city_id))


@router.delete("/{city_id}/days/{day_id}/", response_model=Status,  responses={404: {"model": HTTPNotFoundError}})
async def delete_tracked_day(city_id: UUID, day_id: UUID):
    deleted_count = await TrackedDays.filter(id=day_id, city_id=city_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"TrackedDay {day_id} not found")

    return Status(message=f"Deleted TrackedDay {day_id}")


