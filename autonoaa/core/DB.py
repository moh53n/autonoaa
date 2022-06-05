from ast import Pass
import peewee
import os

from autonoaa.core.Satellite import Satellite

class db_models:
    class BaseModel(peewee.Model):
        class Meta:
            db = peewee.SqliteDatabase(os.getenv('HOME') + "/.autonoaa/database.db")
            #db.create_tables([Pass, Satellite])
            database = db
    
    class Pass(BaseModel):
        sat_id = peewee.IntegerField()
        sat_name = peewee.CharField()
        pass_start = peewee.IntegerField()
        pass_max = peewee.IntegerField()
        pass_end = peewee.IntegerField()
        pass_max_el = peewee.IntegerField()
        pass_az = peewee.IntegerField()
        pass_done = peewee.BooleanField()
    
    class Satellite(BaseModel):
        catnr = peewee.IntegerField(unique = True)
        name = peewee.CharField()
        type_name = peewee.CharField()
        tle = peewee.CharField()
        frequency = peewee.IntegerField()
        bandwidth = peewee.IntegerField()
        service = peewee.CharField()

def connect():
    global db
    db = peewee.SqliteDatabase(os.getenv('HOME') + "/.autonoaa/database.db")
    db.create_tables([db_models.Pass, db_models.Satellite])
    return db

def get_all_passes():
    return db_models.Pass.select().where(db_models.Pass.pass_done == False)

def new_pass(sat_id: int, sat_name: str, pass_start: int, pass_max: int, pass_end: int, pass_max_el: int, pass_az: int):
    db_models.Pass.create(sat_id = sat_id, sat_name = sat_name, pass_start = pass_start, pass_max = pass_max, pass_end = pass_end, pass_max_el = pass_max_el, pass_az = pass_az, pass_done = False)

def pass_set_done(pass_id: int):
    pass_ = db_models.Pass.get(db_models.Pass.id == pass_id)
    pass_.pass_done = True
    pass_.save()

def get_all_satellites():
    return db_models.Satellite.select()

def new_satellite(catnr: int, name: str, type_name: str, tle: str, frequency: int, bandwidth: int, service: str):
    db_models.Satellite.create(catnr = catnr, name = name, type_name = type_name, tle = tle, frequency = frequency, bandwidth = bandwidth, service = service)
