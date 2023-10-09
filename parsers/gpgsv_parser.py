from parsers.base_parser import BaseNMEAParser
from utils.logger import Logger


class GPGSVParser(BaseNMEAParser):
    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger(__name__)

    def parse(self, timestamp: float, fields: list) -> dict:
        """
        Parse the GPGSV sentence fields.
        """
        try:
            total_messages = int(fields[0]) if fields[0] else 0
            message_number = int(fields[1]) if fields[1] else 0
            satellites_in_view = int(fields[2]) if fields[2] else 0

            # Extract satellite IDs
            satellite_data = fields[3:]
            satellite_ids = [
                satellite_data[i] for i in range(0, len(satellite_data), 4)
            ]

            return {
                "timestamp": timestamp,
                "total_messages": total_messages,
                "message_number": message_number,
                "satellites_in_view": satellites_in_view,
                "satellite_ids": satellite_ids,
            }
        except ValueError as e:
            self.logger.error(f"Error parsing GPGSV sentence: {e}")
            return None
