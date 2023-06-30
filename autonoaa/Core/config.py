import configparser
import os

#TODO: add conflict policy and min el
def create_config():
    config = configparser.ConfigParser()
    config['Device'] = {'gain': '0.0',
                     'sample_rate': '2400000', #TODO
                     'freq_correction': '0'}
    config['Location'] = {'latitude': '0.0',
                     'longitude': '0.0',
                     'altitude': '0.0'}
    with open(os.getenv('HOME') + "/.autonoaa/config.ini", "w+") as f:
        config.write(f)

def load_config():
    if not os.path.isfile(os.getenv('HOME') + "/.autonoaa/config.ini"):
        create_config()
    conf = configparser.ConfigParser()
    conf.read(os.getenv('HOME') + "/.autonoaa/config.ini")
    return conf