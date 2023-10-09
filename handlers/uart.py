from .base import BaseIO


class UART(BaseIO):
    """
    Represents a UART connection with default values loaded from the configuration.

    This class inherits from `BaseIO` and uses the configuration specified in
    "config/config.yaml" for UART settings unless the `port`, `baudrate`, `parity`,
    and `stopbit` are provided during instantiation.

    Args:
        port (str, optional): UART port.
        baudrate (int, optional): UART baudrate.
        parity (str, optional): UART parity setting ("N" for none, "E" for even, "O" for odd, etc.).
        stopbit (int, optional): UART stop bit setting (1, 1.5, or 2).
    """

    @classmethod
    def __protocol_name__(cls):
        return "UART"

    def __init__(
        self,
        port: str = None,
        baudrate: int = None,
        parity: str = None,
        stopbit: int = None,
    ):
        """
        Initializes the UART instance with the specified port, baudrate, parity, and stopbit.

        Args:
            port (str, optional): UART port.
            baudrate (int, optional): UART baudrate.
            parity (str, optional): UART parity setting ("N" for none, "E" for even, "O" for odd, etc.).
            stopbit (int, optional): UART stop bit setting (1, 1.5, or 2).
        """
        super().__init__()

        config_values = self.load_from_config(type(self).__name__)
        self.port = port or config_values["serial_port"]
        self.baudrate = baudrate or config_values["baudrate"]
        self.parity = parity or config_values.get(
            "parity", "N"
        )  # Default to "N" if not provided
        self.stopbit = stopbit or config_values.get(
            "stopbit", 1
        )  # Default to 1 if not provided
