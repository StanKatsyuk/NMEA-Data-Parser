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

    # Parse the entire log file using the same parser instance
    parser.parse_log_file(input)

    # Fetching parsed data and plotting
    data = parser.get_data()
    if data:
        timestamps = [point[0] for point in data]
        satellite_counts = [point[1] for point in data]
        ttff = parser.get_ttff()
        print(f"Timestamps: {timestamps}")
        print(f"Satellite Counts: {satellite_counts}")
        print(f"TTFF: {ttff}")
        data_plotter.plot_data(timestamps, satellite_counts, ttff)
        if ttff is not None:
            logger.info(f"Time to First Fix (TTFF): {ttff} seconds")
    else:
        logger.warning("No data available to plot.")