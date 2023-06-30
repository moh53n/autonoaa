from ast import Pass
import peewee
import os

class db_models:
    class BaseModel(peewee.Model):
        class Meta:
            db = peewee.SqliteDatabase(os.getenv('HOME') + "/.autonoaa/database.db")
            #db.create_tables([Pass, Satellite])
            database = db
    
    class Pass(BaseModel):
        pass_id = peewee.IntegerField(unique = True, primary_key = True)
        sat_id = peewee.IntegerField()
        pass_start = peewee.DateTimeField()
        pass_end = peewee.DateTimeField()
        pass_max_el = peewee.IntegerField()
        pass_done = peewee.BooleanField()
    
    class Satellite(BaseModel):
        sat_id = peewee.IntegerField(unique = True, primary_key = True)
        catnr = peewee.IntegerField()
        name = peewee.CharField()
        frequency = peewee.IntegerField()
        bandwidth = peewee.IntegerField()
        service = peewee.CharField()
        enabled = peewee.BooleanField()

def connect():
    global db
    db = peewee.SqliteDatabase(os.getenv('HOME') + "/.autonoaa/database.db")
    db.create_tables([db_models.Pass, db_models.Satellite])
    return db

def get_all_passes():
    return db_models.Pass.select().where(db_models.Pass.pass_done == False)

def get_pass(pass_id):
    return db_models.Pass.select().where(db_models.Pass.pass_id == pass_id)

def new_pass(sat_id, pass_start, pass_end, pass_max_el):
    return db_models.Pass.create(sat_id = sat_id, pass_start = pass_start, pass_end = pass_end, pass_max_el = pass_max_el, pass_done = False)

def get_pass_count(sat_id, pass_start):
    return db_models.Pass.select().where(db_models.Pass.sat_id == sat_id, db_models.Pass.pass_start == pass_start).count()

def pass_set_done(pass_id):
    pass_ = db_models.Pass.get(db_models.Pass.id == pass_id)
    pass_.pass_done = True
    pass_.save()

def get_all_satellites():
    return db_models.Satellite.select()

def get_satellite(sat_id):
    return db_models.Satellite.select().where(db_models.Satellite.sat_id == sat_id)

def get_all_enabled_satellites():
    return db_models.Satellite.select().where(db_models.Satellite.enabled == True)

def new_satellite(catnr, name: str, frequency, bandwidth, service: str):
    return db_models.Satellite.create(catnr = catnr, name = name, frequency = frequency, bandwidth = bandwidth, service = service, enabled = True)

def enable_satellite(sat_id):
    sat = db_models.Satellite.get(db_models.Satellite.sat_id == sat_id)
    sat.enabled = True
    sat.save()

def disable_satellite(sat_id):
    sat = db_models.Satellite.get(db_models.Satellite.sat_id == sat_id)
    sat.enabled = False
    sat.save()