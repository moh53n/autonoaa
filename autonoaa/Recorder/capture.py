from time import sleep, time
import os
import datetime
from autonoaa.Core import DB
import subprocess
from autonoaa.satdump import satdump
from crontab import CronTab
from dateutil import tz
from autonoaa.exporters import telegram

METEOR_COMMAND = """timeout "{CAPTURE_TIME}" rtl_fm -M raw -f "{freq}" -p "{FREQ_OFFSET}" -s {BANDWIDTH} -g "{GAIN}" | sox -t raw -r {BANDWIDTH} -c 2 -b 16 -e signed - -t wav "{OUT_FILE}" rate 96k"""
NOAA_COMMAND = """timeout "{CAPTURE_TIME}" rtl_fm -f "{freq}" -p "{FREQ_OFFSET}" -s {BANDWIDTH} -g "{GAIN}" -E wav -E deemp -F 9 - | sox -t raw -e signed -c 1 -b 16 -r {BANDWIDTH} - "{OUT_FILE}" rate 11025"""

def rec(id, device_conf, satellite, duration):
    if (satellite.service).lower() == "apt" or (satellite.service).lower() == "fm":
        cmd_format = NOAA_COMMAND
    else:
        cmd_format = METEOR_COMMAND

    cmd = cmd_format.format(
        CAPTURE_TIME = duration,
        freq = satellite.frequency,
        FREQ_OFFSET = device_conf.freq_correction,
        BANDWIDTH = satellite.bandwidth,
        GAIN = device_conf.gain,
        OUT_FILE = os.getenv('HOME') + "/.autonoaa/captures/" + f"{id}.wav"
    )
    print(cmd)
    subprocess.check_output(cmd, shell=True)

def run(id, device_conf, satellite, duration: int):
    rec(id, device_conf, satellite, duration)
    try:
        satdump(id, satellite, f"{id}.wav")
    except:
        pass #TODO: LOG

def capture(pass_id, device, config):
    cron = CronTab(user=True)
    cron.remove_all(comment=f'autonoaa-pass-{str(pass_id)}')
    cron.write()

    pass_ = DB.get_pass(pass_id)

    if len(pass_) == 0:
        print("Pass not exists")
        return False
    if pass_[0].pass_done:
        print("Pass already completed")
        return False

    DB.pass_set_done(pass_id)
    sat = DB.get_satellite(pass_[0].sat_id)

    start = datetime.datetime.strptime(pass_[0].pass_start, "%Y-%m-%d %H:%M:%S.%f%z")
    end = datetime.datetime.strptime(pass_[0].pass_end, "%Y-%m-%d %H:%M:%S.%f%z")

    if datetime.datetime.now().replace(tzinfo=tz.tzlocal()) > end:
        print("Pass time expired")
        return False

    duration = (end - start).total_seconds()

    id = sat[0].name + "-" + str(int(time()))  # FIXME

    run(id, device, sat[0], duration)

    if config['TelegramExporter'].getboolean("telegram_enabled"):
        telegram.send(
            config,
            os.getenv("HOME") + "/.autonoaa/captures/" + id,
            pass_[0].pass_max_el,
            start.strftime("%Y-%m-%d %H:%M %z"),
            sat[0].name
        )
