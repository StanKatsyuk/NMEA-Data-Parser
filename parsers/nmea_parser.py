import re
from utils.logger import Logger
from data_types.nmea import NMEASentence
from handlers.base import BaseIO
from parsers.gpgga_parser import GPGGAParser
from parsers.gprmc_parser import GPRMCParser
from parsers.gpgsa_parser import GPGSAParser
from parsers.gngsa_parser import GNGSAParser

logger = Logger(__name__)

class NMEAParser(BaseIO):
    def __init__(self, config_path: str = None, input_file: str = None):
        super().__init__(config_path)

        nmea_log_config = self.load_from_config("NMEA_LOGFILE")

        self.timestamp_prefix = nmea_log_config.get("timestamp_prefix", "t=")
        self.field_separator = nmea_log_config.get("field_separator", ",")
        self.nmea_type_prefix = nmea_log_config.get("nmea_type_prefix", "$")

        self.parsers = {
            NMEASentence.GPGGA: GPGGAParser(),
            NMEASentence.GPRMC: GPRMCParser(),
            NMEASentence.GPGSA: GPGSAParser(),
            NMEASentence.GNGSA: GNGSAParser()
        }

        self.data = []
        self.log_capture_start_time = None
        self.has_fix = False
        self.input_file = input_file

    def parse_log_file(self, input_file: str):
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not self.has_fix:
                    self.parse_sentence(line)
                else:
                    break

    def parse_sentence(self, sentence: str):
        try:
            timestamp_match = re.search(r't=(\d+\.\d+|\d+)', sentence)
            timestamp_str = timestamp_match.group(1)
            timestamp = float(timestamp_str)

            if self.log_capture_start_time is None:
                self.log_capture_start_time = timestamp
                logger.info(f'Start timestamp for satellite tracking: {self.log_capture_start_time}')

            sentence_type_match = re.search(r'\$([A-Za-z]{5})', sentence)
            if not sentence_type_match:
                logger.error(f"No NMEA sentence type found in: {sentence}")
                return
            sentence_type = sentence_type_match.group(1)

            if self.field_separator in sentence:
                sentence_data = sentence.split(self.field_separator, 1)[1]
            else:
                sentence_data = sentence

            fields = sentence_data.split(self.field_separator)
            parser = self.parsers.get(NMEASentence[sentence_type])

            if parser:
                parsed_data = parser.parse(timestamp, fields)
                if parsed_data:
                    if sentence_type == NMEASentence.GPGGA.name:
                        num_satellites = int(fields[7]) if fields[7] else 0
                        if num_satellites != 0 and self.log_capture_start_time is not None:
                            self.ttff = timestamp - self.log_capture_start_time
                            self.has_fix = True
                            logger.info(f'TTFF time: {self.ttff}, {num_satellites=}')
                            self.data.append((self.ttff, num_satellites))
                            return

        except ValueError as e:
            logger.error(e)

    def get_data(self):
        return self.data

    def get_ttff(self):
        return self.ttff if self.ttff else None
