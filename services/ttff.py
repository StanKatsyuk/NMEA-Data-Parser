class TTFFService:
    def __init__(self):
        self.first_fix_time = None

    def update(self, timestamp, satellite_count):
        # Assuming TTFF is when satellite count is greater than 0
        if satellite_count > 0 and self.first_fix_time is None:
            self.first_fix_time = timestamp

    def get_ttff(self):
        return self.first_fix_time