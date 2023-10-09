from parsers.nmea_parser import NMEAParser
from presentation.data_plotter import DataPlotter
from utils.logger import Logger

logger = Logger(__name__)

def process_offline_file(input: str):
    """
    Processes the offline NMEA log file, parses the sentences to extract the number 
    of satellites tracked at each timestamp, and plots the satellite count as a function of time.

    Args:
    - input (str): Path to the NMEA log file to be processed.

    Note:
    - This function also calculates and logs the Time to First Fix (TTFF) based on the data in the file.
    """
    logger.info(f"Processing input file: {input}")

    # Initialize parser and data plotter
    parser = NMEAParser()
    data_plotter = DataPlotter()

    first_fix_timestamp = None  # Initialize to None
    ttff_calculated = False

    with open(input, 'r') as file:
        for line in file:
            line = line.strip()
            parser.parse_sentence(line)

            # Calculate TTFF if it hasn't been calculated yet
            if not ttff_calculated:
                ttff_calculated = True
                if parser.get_ttff() is not None:
                    first_fix_timestamp = parser.get_ttff()

    # Fetching parsed data and plotting
    timestamps, satellite_counts = zip(*parser.get_data())
    data_plotter.plot_data(timestamps, satellite_counts, first_fix_timestamp)

    logger.info(f"Time to First Fix (TTFF): {first_fix_timestamp} seconds")
