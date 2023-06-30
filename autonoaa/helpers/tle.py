import requests
import os

def setup_tle():
    res = requests.get('https://celestrak.org/NORAD/elements/weather.txt')

    if res.ok:
        with open(os.getenv('HOME') + "/.autonoaa/tle/weather.txt", "w+") as f:
            f.write(res.text)
    else:
        print("Failed to update tle")