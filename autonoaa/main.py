import os
import sys
from autonoaa.Core import config as Conf
from autonoaa.helpers.tle import setup_tle
from autonoaa.helpers.default import add_default_sats
from autonoaa.Core import DB
from autonoaa.Core.scheduler import schedule
from autonoaa.Device import Device
from autonoaa.Recorder.capture import capture
from crontab import CronTab
import re

#TODO: first time setup
#TODO: Add reschedule cronjob
#TODO; Fix package struct and INITs
def main():
    if not os.path.isdir(os.getenv('HOME') + "/.autonoaa"):
        print("Creating autonoaa directory")
        os.mkdir(os.getenv('HOME') + "/.autonoaa")

    config = Conf.load_config()
    device = Device(
        float(config['Device']['gain']),
        int(config['Device']['freq_correction'])
    )

    if not os.path.isdir(os.getenv('HOME') + "/.autonoaa/tle"):
        print("Creating tle directory and updating")
        os.mkdir(os.getenv('HOME') + "/.autonoaa/tle")
        setup_tle()

    if not os.path.isdir(os.getenv('HOME') + "/.autonoaa/captures"):
        print("Creating captures directory")
        os.mkdir(os.getenv('HOME') + "/.autonoaa/captures")

    DB.connect()

    if '-c' in sys.argv:
        pass_id = sys.argv[sys.argv.index('-c') + 1]
        capture(pass_id, device)
        return True
    elif '-r' in sys.argv:
        cron = CronTab(user=True)
        iter = cron.find_comment(re.compile(r"autonoaa-.*"))
        for job in iter:
            cron.remove(job)
        cron.write()
        print("Removed autonoaa cronjobs")
        return True

    sats = DB.get_all_satellites()

    if len(sats) == 0:
        print("Satellite DB empty, adding default satellites in enabled mode (you can disable them manually)") #TODO
        add_default_sats()
        sats = DB.get_all_satellites()

    schedule(config)

if __name__ == "__main__":
    main()