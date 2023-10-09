import time
import serial
import matplotlib.pyplot as plt
from parsers.gpgga_parser import GPGGAParser
from services.ttff import TTFFService
from presentation.data_plotter import DataPlotter
from utils.logger import Logger

def read_live_data(serial_port: str, baudrate: int):
    """
    Reads live NMEA data from a serial port and returns a generator of sentences.

    Args:
        serial_port (str): Serial port name (e.g., '/dev/ttyUSB0').
        baudrate (int): Baud rate for serial communication.

    Yields:
        str: NMEA sentences received from the serial port.
    """
    with serial.Serial(serial_port, baudrate) as ser:
        while True:
            sentence = ser.readline().decode().strip()
            yield sentence

def main(serial_port: str, baudrate: int):
    logger = Logger()
    parser = GPGGAParser()
    ttff_service = TTFFService()
    data_plotter = DataPlotter()

    timestamps = []
    satellite_counts = []

    for sentence in read_live_data(serial_port, baudrate):
        timestamp, satellite_count = parser.parse_sentence(sentence)
        if timestamp is not None and satellite_count is not None:
            timestamps.append(timestamp)
            satellite_counts.append(satellite_count)
            ttff_service.update(timestamp, satellite_count)

            # Check for the end of a GPS scan (e.g., based on a condition)
            if condition_for_scan_end:
                break

    # Post-processing
    data_plotter.plot_data(timestamps, satellite_counts)
    logger.info(f"Time to First Fix (TTFF): {ttff_service.get_ttff()} seconds")

if __name__ == "__main__":
    # Define command-line arguments for live parsing
    import argparse
    parser = argparse.ArgumentParser(description="Live NMEA data parser")
    parser.add_argument("--serial-port", required=True, help="Serial port name (e.g., '/dev/ttyUSB0')")
    parser.add_argument("--baudrate", type=int, required=True, help="Baud rate for serial communication")
    args = parser.parse_args()

    main(args.serial_port, args.baudrate)
