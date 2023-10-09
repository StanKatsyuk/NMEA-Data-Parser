from typing import Optional
from parsers.base_parser import BaseNMEAParser
from utils.logger import Logger

logger = Logger(__name__)

class GPGSAParser(BaseNMEAParser):
    def parse(self, timestamp: float, fields: list[str]) -> dict[str, Optional[str]]:
        """
        Parse a GPGSA NMEA sentence and extract relevant information.

        Args:
            timestamp (float): The timestamp associated with the sentence.
            fields (list[str]): List of fields extracted from the NMEA sentence.

        Returns:
            Dict[str, Optional[str]]: A dictionary containing the parsed data, including:
                - 'timestamp': The timestamp as a float.
                - 'fix_status': Fix status ('No Fix', '2D Fix', '3D Fix') as a string.
                  Defaults to None in case of parsing errors.

            Returns a dictionary with 'fix_status' set to None if parsing fails.
        """
        data = {
            'timestamp': timestamp,
            'fix_status': None  # Default fix status in case of parsing errors
        }
        
        try:
            mode = fields[2]
            if mode == '':
                data['fix_status'] = "No Mode"  # Handle empty string
            else:
                mode = int(mode)
                if mode == 1:
                    data['fix_status'] = "No Fix"
                elif mode == 2:
                    data['fix_status'] = "2D Fix"
                elif mode == 3:
                    data['fix_status'] = "3D Fix"
        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing GPGSA sentence: {','.join(fields)}")
            logger.error(f"{e}")

        return data
