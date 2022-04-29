


class Satellite:
    """
    Satellite class
    """

    name = None
    type_name = None
    tle = None
    frequency = None
    service = None
    config = None
    bandwidth = None

    def __init__(self, name, type_name, tle, frequency, bandwidth, service, config):
        self.name = name
        self.type_name = type_name
        self.tle = tle
        self.frequency = frequency
        self.bandwidth = bandwidth
        self.service = service
        self.config = config