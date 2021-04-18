import os
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import app.cities as cities
import app.ping as ping


app = FastAPI()

app.include_router(ping.router)
app.include_router(cities.router, prefix="/cities", tags=["cities"])

register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL"),
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
