class Satellite:
    """
    Satellite class
    """

    name = None
    type_name = None
    tle = None
    frequency = None
    service = None
    bandwidth = None

    def __init__(self, name: str, type_name: str, tle: str, frequency: int, bandwidth: int, service: str):
        self.name = name
        self.type_name = type_name
        self.tle = tle
        self.frequency = frequency
        self.bandwidth = bandwidth
        self.service = service