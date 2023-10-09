from typing import List, Tuple, Optional, Union

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

        self.timestamp_prefix = nmea_log_config.get("timestamp_prefix", "t=")  # Default to "t=" if not found in provided config file
        self.log_delimiter = nmea_log_config.get("delimiter", ", ")  # Default to ", " if not found in provided config file
        self.field_separator = nmea_log_config.get("field_separator", ",")  # Default to ", " if not found in provided config file

        # Dictionary mapping NMEA sentence prefixes to their respective parsers
        self.parsers = {
            NMEASentence.GPGGA: GPGGAParser(),
            NMEASentence.GPRMC: GPRMCParser(),
            NMEASentence.GPGSA: GPGSAParser(),
            NMEASentence.GNGSA: GNGSAParser()
        }
        
        # List to store parsed data
        self.data: List[Tuple[float, int]] = []
        
        # Time to First Fix (initialized to None and updated when first fix is identified)
        self.ttff: Optional[float] = None

    def parse_sentence(self, sentence: str) -> None:
        """
        Parse an individual NMEA sentence.
        
        Args:
            sentence (str): Raw NMEA sentence.
        """
        try:
            # Extract timestamp using the loaded prefix
            if sentence.startswith(self.timestamp_prefix):
                timestamp_str, sentence_part = sentence.split(self.log_delimiter, 1)
                timestamp = float(timestamp_str[len(self.timestamp_prefix):])  # Removing prefix and converting to float
            else:
                logger.error(f"Unexpected prefix in sentence: {sentence}")
                return

            fields = sentence_part.split(self.field_separator)
            sentence_type = fields[0]
            
            # Fetch the parser for the given sentence type
            parser = self.parsers.get(sentence_type)
            
            # If parser exists, parse the sentence
            if parser:
                result = parser.parse(timestamp, fields)
                if 'timestamp' in result and 'satellites_tracked' in result:
                    self.data.append((result['timestamp'], result['satellites_tracked']))
                    
                    # Update Time to First Fix if satellites are being tracked and ttff is not yet set
                    if self.ttff is None and result['satellites_tracked'] > 0:
                        self.ttff = result['timestamp']

        except ValueError:
            logger.error(f"Error parsing sentence: {sentence}")

    def get_data(self) -> List[Tuple[float, int]]:
        """
        Return parsed data.
        
        Returns:
            List[Tuple[float, int]]: List of tuples with timestamp and number of satellites tracked.
        """
        return self.data

    def get_ttff(self) -> Optional[float]:
        """
        Return time to first fix.
        
        Returns:
            Optional[float]: Time to First Fix in seconds if available, else None.
        """
        return self.ttff
