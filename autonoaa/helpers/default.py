from autonoaa.Core import DB

def add_default_sats():
    DB.new_satellite(25338, "NOAA 15", 137620000, 40000, "APT")
    print("Added NOAA 15")
    DB.new_satellite(28654, "NOAA 18", 137912500, 40000, "APT")
    print("Added NOAA 18")
    DB.new_satellite(33591, "NOAA 19", 137100000, 40000, "APT")
    print("Added NOAA 19")
    DB.new_satellite(57166, "METEOR-M2 3", 137900000, 140000, "LRPT")
    print("Added METEOR-M2 3")