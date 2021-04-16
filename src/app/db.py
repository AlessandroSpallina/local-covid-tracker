import os
from databases import Database
from sqlalchemy import Column, Float, Integer, MetaData, String, Table, create_engine
from sqlalchemy.sql import func


DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# TODO: this should be in english!
cities = Table(
    "cities",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("codice_comune", Integer, unique=True),
    Column("distretto", Integer),
    Column("denominazione_comune", String(50), unique=True),
    Column("lat", Float),
    Column("long", Float),
    # TODO: reference to the mayor
)

# databases query builder
database = Database(DATABASE_URL)
