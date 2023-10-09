from enum import Enum

class NMEASentence(Enum):
    GPGGA = "GPGGA"
    GPRMC = "GPRMC"
    GPGSA = "GPGSA"
    GNGSA = "GNGSA"

class NMEAField(Enum):
    UTC_TIME = 1 
    LATITUDE = 2
    LONGITUDE = 3
    SATELLITES_TRACKED = 7
    FIX_STATUS = 6
