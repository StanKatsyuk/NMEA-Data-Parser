from typing import Optional
from parsers.base_parser import BaseNMEAParser
from utils.logger import Logger

logger = Logger(__name__)

class GPRMCParser(BaseNMEAParser):
    def parse(self, timestamp: float, fields: list[str]) -> Optional[dict[str, str]]:
        """
        Parse a GPRMC NMEA sentence and extract relevant information.

        Args:
            timestamp (float): The timestamp associated with the sentence.
            fields (list[str]): List of fields extracted from the NMEA sentence.

        Returns:
            Optional[Dict[str, str]]: A dictionary containing the parsed data, including:
                - 'timestamp': The timestamp as a float.
                - 'fix_status': GPS data status ('A' = data valid, 'V' = data not valid).

            Returns None if parsing fails.
        """
        data = {}
        try:
            data['timestamp'] = timestamp
            data['fix_status'] = fields[2]  # 'A' = data valid, 'V' = data not valid
            return data
        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing GPRMC sentence: {','.join(fields)}")
            logger.error(f"Error details: {str(e)}")
            
            return None
