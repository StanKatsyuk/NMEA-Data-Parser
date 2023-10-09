import click

from utils.offline_parser import process_offline_file
from utils.live_parser import read_live_data

@click.group()
def main():
    pass

@main.command(name="process-offline-file")  # Use the same name as the actual command
@click.option('--input', '-i', type=click.Path(exists=True), required=True, help='Path to the NMEA log file.')
def offline_parser(input: str):
    """
    Parses the offline NMEA log file and plots the number of satellites tracked as a function of time and outputs time to first fix (TTFF)
    """
    process_offline_file(input)

# TODO(Stan) Implement this
# @main.command()
# @click.option('--serial-port', required=True, help='Serial port name (e.g., "/dev/ttyUSB0").')
# @click.option('--baudrate', type=int, required=True, help='Baud rate for serial communication.')
# def live_parser(serial_port: str, baudrate: int):
#     """
#     Parses live NMEA data.
#     """
#     import live_parser  # Import the live_parser script
#     live_parser.main(serial_port, baudrate)

if __name__ == "__main__":
    main()
