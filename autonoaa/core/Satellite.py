class Satellite:
    """
    Satellite class
    """

    id = None
    catnr = None
    name = None
    type_name = None
    tle = None
    frequency = None
    service = None
    bandwidth = None

    def __init__(self, id: int, catnr: int, name: str, type_name: str, tle: str, frequency: int, bandwidth: int, service: str):
        self.id = id
        self.catnr = catnr
        self.name = name
        self.type_name = type_name
        self.tle = tle
        self.frequency = frequency
        self.bandwidth = bandwidth
        self.service = service