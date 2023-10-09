from typing import Optional
from parsers.base_parser import BaseNMEAParser
from utils.logger import Logger

logger = Logger(__name__)

class GPGGAParser(BaseNMEAParser):
    def parse(self, timestamp: float, fields: list[str]) -> dict[str, Optional[str]]:
        """
        Parse a GPGGA NMEA sentence and extract relevant information.

        Args:
            timestamp (float): The timestamp associated with the sentence.
            fields (list[str]): List of fields extracted from the NMEA sentence.

        Returns:
            Dict[str, Optional[str]]: A dictionary containing the parsed data, including:
                - 'timestamp': The timestamp as a float.
                - 'fix_status': Fix status ('No Fix', '2D Fix', '3D Fix') as a string.
                  Defaults to None in case of parsing errors.
                - 'satellites_tracked': Number of satellites tracked as a string.
                  Defaults to None in case of parsing errors.

            Returns a dictionary with None values for fix_status and satellites_tracked if parsing fails.
        """
        data = {
            'timestamp': timestamp,
            'fix_status': None,  # Default fix status in case of parsing errors
            'satellites_tracked': None  # Default value in case of parsing errors
        }
        
        try:
            if len(fields) >= 8:
                data['fix_status'] = fields[6]  # GPS fix status (0=invalid, 1=GPS fix, 2=Diff)
        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing GPGGA sentence: {','.join(fields)}")
            logger.error(f"{str(e)}")

        return data
