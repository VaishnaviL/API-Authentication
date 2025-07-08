import logging
import os
from datetime import datetime

class CustomLogger:
    default_log_directory = "/Logging/logs"

    def __init__(self, logger_name=None, dir_name=None):
        self.logger_name = logger_name or __name__
        self.dir_name = dir_name or self.default_log_directory

        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # Ensure the specified directory exists within the default_log_directory
        logs_directory = os.path.join(os.path.dirname(__file__), self.default_log_directory)
        os.makedirs(logs_directory, exist_ok=True)

        # Create the specified subdirectory within default_log_directory
        specified_logs_directory = os.path.join(logs_directory, self.dir_name)
        os.makedirs(specified_logs_directory, exist_ok=True)

        log_file = self.get_log_file_path()
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Check if logger has handlers already to avoid adding multiple handlers
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

    def get_log_file_path(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        log_file_name = f"{current_date}.log"
        # log_file_name = f"2024-06-14.log"

        # Use the specified directory for logs
        log_file_path = os.path.join(os.path.dirname(__file__), self.default_log_directory, self.dir_name, log_file_name)
        return log_file_path


