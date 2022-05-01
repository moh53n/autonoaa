class config:

    gain = None
    sample_rate = None
    freq_correction = None

    def __init__(self, gain: float, sample_rate: int, freq_correction: float):
        self.gain = gain
        self.sample_rate = sample_rate
        self.freq_correction = freq_correction
