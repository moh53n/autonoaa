from pyorbital.orbital import Orbital
from autonoaa.Core import DB
import os
import datetime
from dateutil import tz
from crontab import CronTab

def new_pass(sat_id, pass_start, pass_end, pass_max_el):
    if DB.get_pass_count(sat_id, pass_start) > 0:
        print('Pass already exists')
    else:
        cron = CronTab(user=True)
        pass_id = DB.new_pass(sat_id, pass_start, pass_end, pass_max_el)
        bin_path = os.getenv("HOME") + "/.local/bin/autonoaa"
        job = cron.new(command=f'{bin_path} -c {str(pass_id)}', comment=f'autonoaa-pass-{str(pass_id)}')
        job.minute.on(pass_start.minute) #FIXME seconds
        job.hour.on(pass_start.hour)
        cron.write()

def schedule(config):
    enabled_sats = DB.get_all_enabled_satellites()
    for sat in enabled_sats:
        passes = (
            Orbital(
                sat.name, tle_file=os.getenv("HOME") + "/.autonoaa/tle/weather.txt"
            ).get_next_passes(
                datetime.datetime.utcnow(),
                24,
                float(config["Location"]["longitude"]),
                float(config["Location"]["latitude"]),
                float(config["Location"]["altitude"])/1000
            )
        )
        for pass_ in passes:
            print(pass_)
            start = (pass_[0].replace(tzinfo=tz.tzutc())).astimezone(tz.tzlocal())
            end = (pass_[1].replace(tzinfo=tz.tzutc())).astimezone(tz.tzlocal())
            new_pass(sat.sat_id, start, end, 0) #FIXME
