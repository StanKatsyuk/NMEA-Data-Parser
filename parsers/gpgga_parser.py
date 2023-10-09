from utils.logger import Logger
from parsers.base_parser import BaseNMEAParser

logger = Logger(__name__)

class GPGGAParser(BaseNMEAParser):

    def parse(self, fields):
        data = {}
        try:
            data['timestamp'] = int(fields[1][:6])
            data['satellites_tracked'] = int(fields[7])
            data['fix_status'] = int(fields[6])
            return data
        except ValueError:
            logger.error(f"Error parsing GPGGA sentence: {','.join(fields)}")
            return None
