from parsers.nmea_parser import NMEAParser
from presentation.data_plotter import DataPlotter
from utils.logger import Logger


class OfflineNMEAProcessor:
    def __init__(self, input_file: str):
        """
        Initializes the OfflineNMEAProcessor.

        Args:
        - input_file (str): Path to the NMEA log file to be processed.
        """
        self.input_file = input_file
        self.logger = Logger(__name__)

    def process(self):
        """
        Processes the offline NMEA log file, parses the sentences to extract the number
        of satellites tracked at each timestamp, and plots the satellite count as a function of time.

        Note:
        - This function also calculates and logs the Time to First Fix (TTFF) based on the data in the file.
        """
        self.logger.info(f"Processing input file: {self.input_file}")

        # Initialize parser and data plotter
        parser = NMEAParser()
        data_plotter = DataPlotter()

        # Parse the entire log file
        parser.parse_log_file(self.input_file)

        # Fetching parsed data and plotting
        data = parser.get_data()
        if data:
            ttff = parser.get_ttff()
            data_plotter.plot_data(data, ttff)
            if ttff is not None:
                self.logger.info(f"Time to First Fix (TTFF): {ttff} seconds")
        else:
            self.logger.warning("No data available to plot.")
