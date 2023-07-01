import subprocess
import os

SATDUMP_COMMAND = """satdump {pipeline} {input_format} "{file_path}" "{output_path}" --samplerate {sample_rate} --baseband_format {format}"""

def satdump(id, satellite, file_name):
    if (satellite.service).lower() == "apt":
        cmd = SATDUMP_COMMAND.format(
            pipeline = "noaa_apt",
            file_path = os.getenv('HOME') + "/.autonoaa/captures/" + file_name,
            output_path = os.getenv('HOME') + "/.autonoaa/captures/" + id,
            sample_rate = 11025,
            format = "s16",
            input_format = "wav"
        )
    elif (satellite.service).lower() == "lrpt":
        cmd = SATDUMP_COMMAND.format(
            pipeline = "meteor_m2-x_lrpt",
            file_path = os.getenv('HOME') + "/.autonoaa/captures/" + file_name,
            output_path = os.getenv('HOME') + "/.autonoaa/captures/" + id,
            sample_rate = 96e3,
            format = "s16",
            input_format = "baseband"
        )
    else:
        print("Satellite service not supported, capture not processed")
        return False

    subprocess.check_output(cmd, shell=True)