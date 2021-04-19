from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Cities(models.Model):
    id = fields.UUIDField(pk=True)
    codice_comune = fields.IntField(unique=True)
    distretto = fields.IntField()
    denominazione_comune = fields.CharField(unique=True, max_length=50)
    lat = fields.FloatField()
    long = fields.FloatField()
    tracked_days = fields.ReverseRelation["TrackedDays"]

City_Pydantic = pydantic_model_creator(Cities, name="City")
CityIn_Pydantic = pydantic_model_creator(Cities, name="CityIn", exclude_readonly=True)


class TrackedDays(models.Model):
    id = fields.UUIDField(pk=True)
    data = fields.DateField()
    ricoverati_con_sintomi = fields.IntField(null=True)
    terapia_intensiva = fields.IntField(null=True)
    totale_ospedalizzati = fields.IntField(null=True)
    isolamento_domiciliare = fields.IntField(null=True)
    totale_positivi = fields.IntField(null=True)
    variazione_totale_positivi = fields.IntField(null=True)
    nuovi_positivi = fields.IntField(null=True)
    dimessi_guariti = fields.IntField(null=True)
    deceduti = fields.IntField(null=True)
    totale_casi = fields.IntField(null=True)
    tamponi = fields.IntField(null=True)
    casi_testati = fields.IntField(null=True)
    ingressi_terapia_intensiva = fields.IntField(null=True)
    note = fields.CharField(null=True, max_length=256)
    note_test = fields.CharField(null=True, max_length=256)
    note_casi = fields.CharField(null=True, max_length=256)
    city = fields.ForeignKeyField('models.Cities', related_name='tracked_days')

    class Meta:
        unique_together=(("data", "city"), )


TrackedDay_Pydantic = pydantic_model_creator(TrackedDays, name="TrackedDay")
TrackedDayIn_Pydantic = pydantic_model_creator(TrackedDays, name="TrackedDayIn", exclude_readonly=True)

