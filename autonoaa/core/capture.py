from . import Satellite
import rtlsdr
from . import Device
import numpy
from time import sleep, time
import threading
from ..helpers import wavfile
import os
import datetime
from . import process
import scipy.signal

class Buffer:
    id = None

    def __init__(self) -> None:
        self.id = str(int(time()))

    def _read_in_chunks(self, file_object, chunk_size = 1024 * 1024 * 10):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def buff_handler(self, samples, context):
        """
        Handler for the buffer.
        """
        with open(self.id + ".tmp", 'ab') as f:
            coef = 250000 / context.sample_rate
            samples_n = int(coef * len(samples))
            samples = scipy.signal.resample(samples, samples_n)
            samples.astype(numpy.complex64).tofile(f)

    def wav(self, filename, sample_rate):
        """
        Save the buffer to a file.
        """
        flag = False
        with open(self.id + '.tmp', 'rb') as f:
            for chunk in self._read_in_chunks(f):
                buff = numpy.frombuffer(chunk, dtype=numpy.complex64)
                print(buff)
                print(buff.shape)
                wav_samples = numpy.zeros((len(buff), 2), dtype=numpy.float32)
                wav_samples[...,0] = buff.real
                wav_samples[...,1] = buff.imag
                with open(filename + '.wav', 'ab') as f2:
                    wavfile.write(f2, 250000, wav_samples, flag, os.path.getsize(self.id + '.tmp'))
                flag = True
        os.rename(self.id + '.tmp', filename + '.iq')

def rec(id: str, device_conf: Device.config, satellite: Satellite.Satellite, duration: int):
    """
    Captures data from the satellite.
    """
    sdr = rtlsdr.RtlSdr()
    sdr.sample_rate = device_conf.sample_rate
    sdr.gain = device_conf.gain
    #sdr.freq_correction = device_conf.freq_correction
    sdr.center_freq = satellite.frequency
    sdr.bandwidth = satellite.bandwidth
    buff = Buffer()
    thr = threading.Thread(target=sdr.read_samples_async, args=(buff.buff_handler, 512 * 1024), kwargs={})
    thr.start()
    sleep(duration + 5)
    sdr.cancel_read_async()
    thr.join()
    buff.wav(id + "(IQ)", sdr.sample_rate)

def run(device_conf: Device.config, satellite: Satellite.Satellite, duration: int):
    """
    Run a capture
    """
    id = satellite.name + "-" + str(int(time()))
    rec(id, device_conf, satellite, duration)
    if (satellite.service).lower() == "apt":
        process.apt_process(id, device_conf.sample_rate, satellite.bandwidth)
    else:
        print("Satellite service not supported.")