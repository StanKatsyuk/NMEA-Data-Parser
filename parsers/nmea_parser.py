import re
from typing import Optional
from utils.logger import Logger
from data_types.nmea import NMEASentence
from handlers.base import BaseIO
from parsers.gpgga_parser import GPGGAParser
from parsers.gprmc_parser import GPRMCParser
from parsers.gpgsa_parser import GPGSAParser
from parsers.gngsa_parser import GNGSAParser

logger = Logger(__name__)

class NMEAParser(BaseIO):
    """
    NMEA Parser class.
    
    This class is responsible for parsing NMEA sentences from various sources.
    Each NMEA sentence type is handled by its respective parser.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize the NMEAParser.
        
        Args:
            config_path (str, optional): Path to the configuration file. Defaults to None which uses the default path in BaseIO.
        """
        super().__init__(config_path)

        # Load config data
        nmea_log_config = self.load_from_config("NMEA_LOGFILE")

        # Set log specific params
        self.timestamp_prefix = nmea_log_config.get("timestamp_prefix", "t=")  # Default to "t=" if not found in provided config file
        self.log_delimiter = nmea_log_config.get("delimiter", ", ")  # Default to ", " if not found in provided config file
        self.field_separator = nmea_log_config.get("field_separator", ",")  # Default to ", " if not found in provided config file
        self.nmea_type_prefix = nmea_log_config.get("nmea_type_prefix", "$")  # Default to "$" if not found in provided config file

        # Dictionary mapping NMEA sentence prefixes to their respective parsers
        self.parsers = {
            NMEASentence.GPGGA: GPGGAParser(),
            NMEASentence.GPRMC: GPRMCParser(),
            NMEASentence.GPGSA: GPGSAParser(),
            NMEASentence.GNGSA: GNGSAParser()
        }
        
        # List to store parsed data
        self.data: list[tuple[float, int]] = []
        
        # Time to First Fix (initialized to None and updated when first fix is identified)
        self.ttff: Optional[float] = None

    def parse_sentence(self, sentence: str) -> None:
        """
        Parse an individual NMEA sentence.

        Args:
            sentence (str): Raw NMEA sentence.
        """
        try:
            # Use regex to extract the timestamp
            timestamp_match = re.search(r't=(\d+\.\d+|\d+)', sentence)
            
            if not timestamp_match:
                logger.error(f"No timestamp found in sentence: {sentence}")
                return
            
            timestamp_str = timestamp_match.group(1)
            timestamp = float(timestamp_str)

            # Extract sentence type using regex
            sentence_type_match = re.search(r'\$([A-Za-z]{5})', sentence)

            if sentence_type_match:
                sentence_type = sentence_type_match.group(1)
            else:
                logger.error(f"No NMEA sentence type found in: {sentence}")
                return

            # Check if there is a comma after the timestamp, and split accordingly
            if self.field_separator in sentence:
                sentence_data = sentence.split(self.field_separator, 1)[1]
            else:
                sentence_data = sentence

            fields = sentence_data.split(self.field_separator)

            if not sentence_type:
                logger.error(f"Empty or invalid sentence type: {sentence}")
                return  # Skip further processing for invalid sentence types

            # Fetch the parser for the given sentence type
            parser = self.parsers.get(NMEASentence[sentence_type])

            if parser:
                result = parser.parse(timestamp, fields)

                # Check if the result contains relevant data
                if result and 'timestamp' in result and 'satellites_tracked' in result:
                        self.data.append((result['timestamp'], result['satellites_tracked']))

                        # Update Time to First Fix if satellites are being tracked and ttff is not yet set
                        if self.ttff is None and result['satellites_tracked'] is not None and result['satellites_tracked'] > 0:
                            self.ttff = result['timestamp']
                else:
                    pass

        except ValueError as e:
            logger.error(e)

    def get_data(self) -> list[tuple[float, int]]:
        """
        Return parsed data.
        
        Returns:
            list[tuple[float, int]]: List of tuples with timestamp and number of satellites tracked.
        """
        return self.data

    def get_ttff(self) -> Optional[float]:
        """
        Return time to first fix.
        
        Returns:
            Optional[float]: Time to First Fix in seconds if available, else None.
        """
        return self.ttff
