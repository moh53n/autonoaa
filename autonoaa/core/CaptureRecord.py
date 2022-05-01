import datetime

class CaptureRecord:

    capture_id = None
    sat_name = None
    capture_datetime = None

    def __init__(self, capture_id: str, sat_name: str, capture_datetime: datetime.datetime):
        self.capture_id = capture_id
        self.sat_name = sat_name
        self.capture_datetime = capture_datetime
