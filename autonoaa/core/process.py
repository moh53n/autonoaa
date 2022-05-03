from scipy.signal import firwin, lfilter
import numpy
import scipy
from ..helpers import wavfile
import os
from ..decoders import APT
import struct

class demodulator:
    def fm_demod(x, df=1.0, fc=0.0):
        # https://stackoverflow.com/questions/60193112/python-fm-demod-implementation
        n = numpy.arange(len(x))
        rx = x*numpy.exp(-1j*2*numpy.pi*fc*n)
        phi = numpy.arctan2(numpy.imag(rx), numpy.real(rx))
        y = numpy.diff(numpy.unwrap(phi)/(2*numpy.pi*df))
        return y

def read_in_chunks(file_object, chunk_size = 1024 * 1024 * 10):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

def apt_process(id, sample_rate, bandwidth):
    flag = False
    with open(id + "(IQ).iq", 'rb') as f:
        for chunk in read_in_chunks(f, 8*sample_rate*30):
            buff = numpy.frombuffer(chunk, dtype=numpy.complex64)
            print(buff)
            buff = bandpass_filter(buff, sample_rate, bandwidth)
            buff = demodulator.fm_demod(buff)
            coef = 20800 / sample_rate
            samples = int(coef * len(buff))
            buff = scipy.signal.resample(buff, samples)
            with open(id + "(FM).wav", 'ab') as f2:
                size = wavfile.write(f2, 20800, ((buff.astype(numpy.float32)) * 32767).astype(numpy.int16), flag, os.path.getsize(id + "(IQ).iq")//2)
            flag = True
    with open(id + "(FM).wav", 'r+b') as fid:
        fid.seek(4)
        fid.write(struct.pack('<I', size-8))
    apt = APT(id + "(FM).wav")
    apt.decode(id + '.png')

def bandpass_filter(x, fs, cutoff):
    # https://www.programcreek.com/python/example/100540/scipy.signal.firwin
    nyquist = fs // 2
    norm_cutoff = cutoff / nyquist
    fil = firwin(255, norm_cutoff)
    res = lfilter(fil, 1, x)
    return res

def resample(in_filename, out_filename, to_rate):
    # https://github.com/zacstewart/apt-decoder/blob/master/resample.py
    (rate, signal) = scipy.io.wavfile.read(in_filename)

    if rate != to_rate:
        coef = to_rate / rate
        samples = int(coef * len(signal))
        signal = scipy.signal.resample(signal, samples)
        scipy.io.wavfile.write(out_filename, to_rate, signal)