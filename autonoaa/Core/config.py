import configparser
import os

#TODO: add conflict policy and min el
def create_config():
    print("Config not exists, Generating one...")
    gain = float(input("Enter the SDR gain: "))
    freq_correction = int(input("Enter the SDR frequency correction (PPM): "))
    lat = float(input("Enter the latitude: "))
    lon = float(input("Enter the longitude: "))
    alt = int(input("Enter the altitude (meters): "))
    config = configparser.ConfigParser()
    config['Device'] = {'gain': gain,
                     'freq_correction': freq_correction}
    config['Location'] = {'latitude': lat,
                     'longitude': lon,
                     'altitude': alt}
    with open(os.getenv('HOME') + "/.autonoaa/config.ini", "w+") as f:
        config.write(f)

def load_config():
    if not os.path.isfile(os.getenv('HOME') + "/.autonoaa/config.ini"):
        create_config()
    conf = configparser.ConfigParser()
    conf.read(os.getenv('HOME') + "/.autonoaa/config.ini")
    return conf