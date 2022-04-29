

class CaptureRecord:

    capture_id = None
    sat_name = None
    datetime = None

    def __init__(self, capture_id, sat_name, datetime):
        self.capture_id = capture_id
        self.sat_name = sat_name
        self.datetime = datetime
