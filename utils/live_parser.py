import serial
from parsers.gpgga_parser import GPGGAParser
from services.ttff import TTFFService
from presentation.data_plotter import DataPlotter
from utils.logger import Logger


class LiveNMEAParser:
    def __init__(
        self, serial_port: str, baudrate: int, parity: int = None, stopbit: int = 1
    ):
        """
        Initialize the LiveNMEAParser.

        Args:
            serial_port (str): Serial port name (e.g., '/dev/ttyUSB0').
            baudrate (int): Baud rate for serial communication.
            parity (int, optional): Parity setting for serial communication. Default is None.
            stopbit (int, optional): Stop bit setting for serial communication. Default is 1.

        Attributes:
            serial_port (str): Serial port name.
            baudrate (int): Baud rate.
            parity (int): Parity setting.
            stopbit (int): Stop bit setting.
            logger (Logger): Logger instance.
            parser (GPGGAParser): NMEA sentence parser.
            ttff_service (TTFFService): TTFF service for tracking time to first fix.
            data_plotter (DataPlotter): Data plotter for visualization.
        """
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbit = stopbit
        self.logger = Logger("logger")
        self.parser = GPGGAParser()
        self.ttff_service = TTFFService()
        self.data_plotter = DataPlotter()

    def read_live_data(self):
        """
        Read live NMEA data from the serial port and yield sentences.

        Yields:
            str: NMEA sentences received from the serial port.
        """
        # Use a context manager for handling serial communication
        with serial.Serial(
            self.serial_port, self.baudrate, parity=self.parity, stopbits=self.stopbit
        ) as ser:
            while True:
                sentence = ser.readline().decode().strip()
                yield sentence

    def parse_and_plot(self):
        """
        Parse live NMEA data, plot the data, and log TTFF.
        """
        timestamps = []
        satellite_counts = []

        for sentence in self.read_live_data():
            timestamp, satellite_count = self.parser.parse_sentence(sentence)
            if timestamp is not None and satellite_count is not None:
                timestamps.append(timestamp)
                satellite_counts.append(satellite_count)
                self.ttff_service.update(timestamp, satellite_count)

                # Check for the end of a GPS scan (e.g., based on a condition)
                if self.is_scan_complete():
                    break

        # Post-processing
        self.data_plotter.plot_data(timestamps, satellite_counts)
        self.logger.info(
            f"Time to First Fix (TTFF): {self.ttff_service.get_ttff()} seconds"
        )

    def is_scan_complete(self):
        """
        This is where we will implement the serial clean up once transmission ends

        Returns:
            bool: True if the scan is complete, False otherwise.
        """
        return False
