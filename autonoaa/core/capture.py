import Satellite
import rtlsdr
import Device
import numpy
from time import sleep, time
import threading
import wavfile
import os

class Buffer:
    id = None

    def __init__(self) -> None:
        self.id = str(int(time()))

    def read_in_chunks(self, file_object, chunk_size = 1024 * 1024 * 10):
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
            samples.tofile(f)

    def wav(self, filename, sample_rate):
        """
        Save the buffer to a file.
        """
        flag = False
        with open(self.id + '.tmp', 'rb') as f:
            for chunk in self.read_in_chunks(f):
                buff = numpy.frombuffer(chunk, dtype=numpy.complex128)
                print(buff)
                print(buff.shape)
                wav_samples = numpy.zeros((len(buff), 2), dtype=numpy.float32)
                wav_samples[...,0] = buff.real
                wav_samples[...,1] = buff.imag
                with open(filename + '.wav', 'ab') as f2:
                    wavfile.write(f2, int(sample_rate), wav_samples, flag, os.path.getsize(self.id + '.tmp'))
                flag = True
        os.rename(self.id + '.tmp', filename + '.iq')

def rec(id: str, device_conf: Device.config, satellite: Satellite.Satellite, duration):
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
    thr = threading.Thread(target=sdr.read_samples_async, args=(buff.buff_handler,200*1024), kwargs={})
    thr.start()
    sleep(duration + 5)
    sdr.cancel_read_async()
    thr.join()
    buff.wav(id + "(IQ)", sdr.sample_rate)

#sat = Satellite.Satellite("test", "testt", "aaa", 104000000, 150000, None, None)
#device = Device.config(49.6, 250000, 0)
#run(device, sat, 60)