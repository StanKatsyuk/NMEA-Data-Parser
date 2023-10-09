from utils.logger import Logger
from parsers.base_parser import BaseNMEAParser

logger = Logger(__name__)

class GPRMCParser(BaseNMEAParser):

    def parse(self, fields):
        # TODO(Stan): Implement parsing logic for GPRMC
        # It is not a requirement for assignment at this time so we just return an empty dict
        return {}
