from typing import Union
from parsers.base_parser import BaseNMEAParser
from utils.logger import Logger


class GPGSAParser(BaseNMEAParser):
    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger(__name__)

    def parse(
        self, timestamp: float, fields: list[str]
    ) -> dict[str, Union[float, str, int]]:
        """
        Parse a GPGSA NMEA sentence and extract relevant information.

        Args:
            timestamp (float): The timestamp associated with the sentence.
            fields (list[str]): List of fields extracted from the NMEA sentence.

        Returns:
            Dict[str, Union[float, str, int]]: A dictionary containing the parsed data, including:
                - 'timestamp': The timestamp as a float.
                - 'fix_status': Fix status ('No Fix', '2D Fix', '3D Fix') as a string.
                - 'num_satellites_tracked': Number of satellites being tracked.

            Returns a dictionary with 'fix_status' and 'num_satellites_tracked' set to None if parsing fails.
        """
        data = {
            "timestamp": timestamp,
            "fix_status": None,  # Default fix status in case of parsing errors
            "num_satellites_tracked": None,  # Default number of satellites in case of parsing errors
        }

        try:
            mode = fields[1]
            if mode == "":
                data["fix_status"] = "No Mode"  # Handle empty string
            elif mode == "1":
                data["fix_status"] = "No Fix"
            elif mode == "2":
                data["fix_status"] = "2D Fix"
            elif mode == "3":
                data["fix_status"] = "3D Fix"

            # Extract satellite IDs
            satellite_ids = fields[2:14]

            # Count non-empty satellite IDs
            num_satellites_tracked = sum(1 for sat_id in satellite_ids if sat_id)
            data["num_satellites_tracked"] = num_satellites_tracked

        except (ValueError, IndexError) as e:
            self.logger.error(f"Error parsing GPGSA sentence: {','.join(fields)}")
            self.logger.error(f"{e}")

        return data
