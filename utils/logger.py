import logging
from pathlib import Path


class Logger:
    def __init__(
        self, name: str, log_file_path: str = None, log_level: int = logging.INFO
    ) -> None:
        """
        A custom logger class that provides file and console logging with flexible log levels.

        Args:
            name (str): The name of the logger.
            log_file_path (str, optional): The path to the log file. If provided, log messages
                will be written to this file. Defaults to None (no log file).
            log_level (int, optional): The log level to set for the logger. Defaults to logging.INFO.

        Attributes:
            logger (logging.Logger): The logger instance.

        Example:
            logger = Logger("my_logger", "my_log.txt")
            logger.log_info("This is an information message.")
            logger.log_warning("This is a warning message.")
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Create a formatter
        formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")

        # Create a file handler if log_file_path is provided
        if log_file_path:
            self.add_file_handler(log_file_path, formatter)

        # Create a console handler
        self.add_console_handler(formatter)

    def add_file_handler(
        self, log_file_path: str, formatter: logging.Formatter
    ) -> None:
        # Ensure the log directory exists
        log_dir = Path(log_file_path).parent
        # Create output dir if it doesn't exist
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create a file handler
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def add_console_handler(self, formatter: logging.Formatter) -> None:
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def exception(self, message: str) -> None:
        self.logger.exception(message)

    def set_log_level(self, log_level: int) -> None:
        self.logger.setLevel(log_level)

    def remove_handlers(self) -> None:
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
