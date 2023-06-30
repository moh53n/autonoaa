class Device:

    gain = None
    freq_correction = None

    def __init__(self, gain: float, freq_correction: float):
        self.gain = gain
        self.freq_correction = freq_correction
