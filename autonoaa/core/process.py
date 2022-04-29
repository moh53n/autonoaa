from scipy.signal import firwin, lfilter
import numpy
import scipy

class demodulator:
    def fm_demod(x, df=1.0, fc=0.0):
        # https://stackoverflow.com/questions/60193112/python-fm-demod-implementation
        n = numpy.arange(len(x))
        rx = x*numpy.exp(-1j*2*numpy.pi*fc*n)
        phi = numpy.arctan2(numpy.imag(rx), numpy.real(rx))
        y = numpy.diff(numpy.unwrap(phi)/(2*numpy.pi*df))
        return y

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