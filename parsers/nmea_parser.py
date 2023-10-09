import re
from utils.logger import Logger
from data_types.nmea import NMEASentence
from handlers.base import BaseIO
from parsers.gpgga_parser import GPGGAParser
from parsers.gprmc_parser import GPRMCParser
from parsers.gpgsa_parser import GPGSAParser
from parsers.gngsa_parser import GNGSAParser
from enum import Enum


class SatelliteStatus(Enum):
    TRACKED = "tracked"
    IN_VIEW = "in_view"


class FixStatus(Enum):
    FIX_2D = "2D Fix"
    FIX_3D = "3D Fix"


class NMEAParser(BaseIO):
    def __init__(self, config_path: str = None, input_file: str = None):
        super().__init__(config_path)
        self.logger = Logger(__name__)

        nmea_log_config = self.load_from_config("NMEA_LOGFILE")

        self.timestamp_prefix = nmea_log_config.get("timestamp_prefix", "t=")
        self.field_separator = nmea_log_config.get("field_separator", ",")
        self.nmea_type_prefix = nmea_log_config.get("nmea_type_prefix", "$")

        self.parsers = {
            NMEASentence.GPGGA: GPGGAParser(),
            NMEASentence.GPRMC: GPRMCParser(),
            NMEASentence.GPGSA: GPGSAParser(),
            NMEASentence.GNGSA: GNGSAParser(),
        }

        self.data = []
        self.log_capture_start_time = None
        self.has_fix = False
        self.input_file = input_file
        self.ttff = None
        self.num_satellites_in_view = 0  # Initialize the count of satellites in view

    def parse_log_file(self, input_file: str):
        with open(input_file, "r") as file:
            for line in file:
                line = line.strip()
                self.parse_sentence(line)

    def parse_sentence(self, sentence: str):
        try:
            timestamp_match = re.search(r"t=(\d+\.\d+|\d+)", sentence)
            timestamp_str = timestamp_match.group(1)
            timestamp = float(timestamp_str)

            # Add a variable to track the start time of satellite tracking
            if self.log_capture_start_time is None:
                self.log_capture_start_time = timestamp
                self.logger.debug(
                    f"Start timestamp for satellite tracking: {self.log_capture_start_time}"
                )

            sentence_type_match = re.search(r"\$([A-Za-z]{5})", sentence)
            if not sentence_type_match:
                self.logger.error(f"No NMEA sentence type found in: {sentence}")
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
                        num_satellites_in_view = int(fields[7]) if fields[7] else 0
                        self.num_satellites_in_view = (
                            num_satellites_in_view  # Update the count
                        )
                        self.data.append(
                            (
                                timestamp,
                                SatelliteStatus.IN_VIEW.value,
                                num_satellites_in_view,
                            )
                        )

                        # Calculate TTFF based on the first non-zero value of satellites in view
                        if num_satellites_in_view > 0 and self.ttff is None:
                            self.ttff = round(
                                timestamp - self.log_capture_start_time, 2
                            )
                            self.logger.info(f"TTFF time: {self.ttff}")
                    elif sentence_type == NMEASentence.GPGSA.name:
                        num_satellites_tracked = parsed_data["num_satellites_tracked"]
                        if (
                            not self.data
                            or (
                                self.data[-1][1] == SatelliteStatus.IN_VIEW.value
                                and num_satellites_tracked < self.data[-1][2]
                            )
                            or (
                                self.data[-1][1] == SatelliteStatus.TRACKED.value
                                and num_satellites_tracked >= self.data[-1][2]
                            )
                        ):
                            self.data.append(
                                (
                                    timestamp,
                                    SatelliteStatus.TRACKED.value,
                                    num_satellites_tracked,
                                )
                            )
                        if not self.has_fix and parsed_data["fix_status"] in [
                            FixStatus.FIX_2D.value,
                            FixStatus.FIX_3D.value,
                        ]:
                            self.has_fix = True
                            self.ttff = round(
                                timestamp - self.log_capture_start_time, 2
                            )
                            self.logger.info(f"TTFF time: {self.ttff}")

        except ValueError as e:
            self.logger.error(e)

    def get_data(self):
        return self.data

    def get_ttff(self):
        return self.ttff if hasattr(self, "ttff") else None
