class config:

    gain = None
    sample_rate = None
    freq_correction = None

    def __init__(self, gain, sample_rate, freq_correction):
        self.gain = gain
        self.sample_rate = sample_rate
        self.freq_correction = freq_correction
