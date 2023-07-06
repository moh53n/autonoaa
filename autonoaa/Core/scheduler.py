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
        job = cron.new(command=f'/bin/sleep {pass_start.second} && {bin_path} -c {str(pass_id)}', comment=f'autonoaa-pass-{str(pass_id)}')
        job.minute.on(pass_start.minute)
        job.hour.on(pass_start.hour)
        cron.write()

def disable_pass(pass_):
    DB.pass_set_done(pass_['pass_id'])
    cron = CronTab(user=True)
    cron.remove_all(comment=f'autonoaa-pass-{str(pass_["pass_id"])}')
    cron.write()

def resolve_conflicts(config):
    passes_db = DB.get_all_passes()
    passes = []
    prioritize_meteor = config['Passes'].getboolean("prioritize_meteor")

    for pass_ in passes_db:
        sat = DB.get_satellite(pass_.sat_id)
        
        is_lrpt = False
        if (sat[0].service).lower() == "lrpt":
            is_lrpt = True

        entry = {
            'pass_id': pass_.pass_id,
            'pass_start': datetime.datetime.strptime(pass_.pass_start, "%Y-%m-%d %H:%M:%S.%f%z"),
            'pass_end': datetime.datetime.strptime(pass_.pass_end, "%Y-%m-%d %H:%M:%S.%f%z"),
            'pass_max_el': int(pass_.pass_max_el),
            'is_lrpt': is_lrpt
        }
        
        passes.append(entry)

    exclude = []

    for i in range(len(passes)): # WARNING, dirty code, welcome to the jungle
        if i in exclude:  # avoid manipulating the list in iter
            continue
        pass_ = passes[i]
        for j in range(len(passes)):
            pass2 = passes[j]
            if i == j or j in exclude:
                continue
            if pass2['pass_start'] >= pass_['pass_start'] and pass2['pass_start'] <= pass_['pass_end']:
                print(f"Conflict found between pass {pass_['pass_id']} and {pass2['pass_id']}, resolving it...")
                if pass_['is_lrpt'] and prioritize_meteor:
                    if pass2['is_lrpt']:
                        if pass_['pass_max_el'] > pass2['pass_max_el']:
                            disable_pass(pass2)
                            exclude.append(j)
                            print(f"Disabled pass {pass2['pass_id']} in favour of pass {pass_['pass_id']}")
                        else:
                            disable_pass(pass_)
                            exclude.append(i)
                            print(f"Disabled pass {pass_['pass_id']} in favour of pass {pass2['pass_id']}")
                            break
                    else:
                        disable_pass(pass2)
                        exclude.append(j)
                        print(f"Disabled pass {pass2['pass_id']} in favour of pass {pass_['pass_id']}")
                elif pass2['is_lrpt'] and prioritize_meteor:
                    disable_pass(pass_)
                    exclude.append(i)
                    print(f"Disabled pass {pass_['pass_id']} in favour of pass {pass2['pass_id']}")
                    break
                else:
                    if pass_['pass_max_el'] > pass2['pass_max_el']:
                        disable_pass(pass2)
                        exclude.append(j)
                        print(f"Disabled pass {pass2['pass_id']} in favour of pass {pass_['pass_id']}")
                    else:
                        disable_pass(pass_)
                        exclude.append(i)
                        print(f"Disabled pass {pass_['pass_id']} in favour of pass {pass2['pass_id']}")
                        break

        exclude.append(i)

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

            look = Orbital(
                sat.name, tle_file=os.getenv("HOME") + "/.autonoaa/tle/weather.txt"
            ).get_observer_look(
                pass_[2],
                float(config["Location"]["longitude"]),
                float(config["Location"]["latitude"]),
                float(config["Location"]["altitude"])/1000
            )

            if look[1] < float(config['Passes']['min_elevation']):
                print("Pass below the required elevation, ignoring...")
                continue

            start = (pass_[0].replace(tzinfo=tz.tzutc())).astimezone(tz.tzlocal())
            end = (pass_[1].replace(tzinfo=tz.tzutc())).astimezone(tz.tzlocal())
            new_pass(sat.sat_id, start, end, look[1])

    resolve_conflicts(config)

def scheduler_cron():
    cron = CronTab(user=True)
    scheduler_line = False
    reboot_scheduler_line = False
    bin_path = os.getenv("HOME") + "/.local/bin/autonoaa"

    for line in cron.lines:
        if "autonoaa-scheduler" in str(line):
            scheduler_line = True
        if "autonoaa-reboot-scheduler" in str(line):
            reboot_scheduler_line = True

    if not scheduler_line:
        job = cron.new(command=f'{bin_path} -s', comment=f'autonoaa-scheduler')
        job.minute.on(0)
        job.hour.on(1)
        cron.write()

    if not reboot_scheduler_line:
        job = cron.new(command=f'{bin_path} -s', comment=f'autonoaa-reboot-scheduler')
        job.every_reboot()
        cron.write()