import configparser
import os

#TODO: Explain every entry in the README and print the link
def create_config():
    print("Config not exists, Generating one...")
    gain = float(input("Enter the SDR gain: "))
    freq_correction = int(input("Enter the SDR frequency correction (PPM): "))
    lat = float(input("Enter the latitude: "))
    lon = float(input("Enter the longitude: "))
    alt = int(input("Enter the altitude (meters): "))
    min_elevation = float(input("Enter the minimum required elevation: "))
    if input("Do you want to prioritize Meteor satellites over NOAA in a pass conflict? (Y/N): ").lower() == "y":
        prioritize_meteor = True
    else:
        prioritize_meteor = False
    config = configparser.ConfigParser()
    config['Device'] = {'gain': gain,
                     'freq_correction': freq_correction}
    config['Location'] = {'latitude': lat,
                     'longitude': lon,
                     'altitude': alt}
    config['Passes'] = {'min_elevation': min_elevation, 'prioritize_meteor': prioritize_meteor}
    telegram_enabled = False
    telegram_token = ''
    telegram_chat = ''
    if input("Do you want to enable and setup Telegram exporter? (Y/N): ").lower() == "y":
        telegram_enabled = True
        telegram_token = input("Enter the Telegram Bot token: ")
        telegram_chat = input("Enter the Telegram chat ID: ")

    config['TelegramExporter'] = {'telegram_enabled': telegram_enabled,
                     'telegram_token': telegram_token,
                     'telegram_chat': telegram_chat}

    with open(os.getenv('HOME') + "/.autonoaa/config.ini", "w+") as f:
        config.write(f)

def load_config():
    if not os.path.isfile(os.getenv('HOME') + "/.autonoaa/config.ini"):
        create_config()
    conf = configparser.ConfigParser()
    conf.read(os.getenv('HOME') + "/.autonoaa/config.ini")
    return conf