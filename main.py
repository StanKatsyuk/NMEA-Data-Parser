import click

from utils.offline_parser import process_offline_file
from utils.live_parser import LiveNMEAParser

from serial import PARITY_NONE


@click.group()
def main():
    pass


@main.command(name="process-offline-file")  # Use the same name as the actual command
@click.option(
    "--input",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="Path to the NMEA log file.",
)
def offline_parser(input: str):
    """
    Parses the offline NMEA log file and plots the number of satellites tracked as a function of time and outputs time to first fix (TTFF)
    """
    process_offline_file(input)


# Note: This was not tested but is a conceptual approach to using serial to parse data
@main.command(name="process-live-data")
@click.option(
    "--serial-port",
    required=False,
    help='Serial port name (e.g., "/dev/ttyUSB0") - Default: Use value in configs/config.yaml.',
)
@click.option(
    "--baudrate",
    type=int,
    default=9600,
    required=False,
    help="Baud rate for serial communication - Default: Use value in configs/config.yaml.",
)
@click.option(
    "--parity",
    type=click.Choice(["N", "E", "O", "S", "M"]),
    default="N",
    help="Parity setting for serial communication.",
)
@click.option(
    "--stopbit", type=int, default=1, help="Stop bit setting for serial communication."
)
def live_parser(serial_port: str, baudrate: int, parity: int, stopbit: int):
    """
    Parses live NMEA data via the serial poort
    """
    live_parser = LiveNMEAParser(serial_port, baudrate, parity, stopbit)
    live_parser.parse_and_plot()


if __name__ == "__main__":
    main()
