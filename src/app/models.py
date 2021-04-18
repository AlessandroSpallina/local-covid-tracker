from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Cities(models.Model):
    id = fields.UUIDField(pk=True)
    codice_comune = fields.IntField(unique=True)
    distretto = fields.IntField()
    denominazione_comune = fields.CharField(unique=True, max_length=50)
    lat = fields.FloatField()
    long = fields.FloatField()

City_Pydantic = pydantic_model_creator(Cities, name="City")
CityIn_Pydantic = pydantic_model_creator(Cities, name="CityIn", exclude_readonly=True)
