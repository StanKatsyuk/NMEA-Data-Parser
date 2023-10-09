from .base import BaseIO

class UART(BaseIO):
    """
    Represents a UART connection with default values loaded from the configuration.

    This class inherits from `BaseIO` and uses the configuration specified in 
    "config/config.yaml" for UART settings unless the `port` and `baudrate` are 
    provided during instantiation.

    Args:
        port (str, optional): UART port.
        baudrate (int, optional): UART baudrate.
    """
    
    def __init__(self, port: str = None, baudrate: int = None):
        """
        Initializes the UART instance with the specified port and baudrate.

        Args:
            port (str, optional): UART port.
            baudrate (int, optional): UART baudrate.
        """
        super().__init__()
        
        config_values = self._load_from_config(type(self).__name__)
        self.port = port or config_values['port']
        self.baudrate = baudrate or config_values['baudrate']
