from app.api.models import CitySchema
from app.db import cities, database


async def post(payload: CitySchema):
    query = cities.insert().values(
        codice_comune=payload.codice_comune,
        distretto=payload.distretto,
        denominazione_comune=payload.denominazione_comune,
        lat=payload.lat,
        long=payload.long,
    )
    return await database.execute(query=query)


async def get(id: int):
    query = cities.select().where(id == cities.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = cities.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: CitySchema):
    query = (
        cities
        .update()
        .where(id == cities.c.id)
        .values(
            codice_comune=payload.codice_comune,
            distretto=payload.distretto,
            denominazione_comune=payload.denominazione_comune,
            lat=payload.lat,
            long=payload.long,
        )
        .returning(cities.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = cities.delete().where(id == cities.c.id)
    return await database.execute(query=query)
