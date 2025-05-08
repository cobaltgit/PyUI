import logging
import os
import sys

class StreamToLogger:
    """Redirect writes to a logger."""
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self._buffer = ""

    def write(self, message):
        message = message.strip()
        if message:
            self.logger.log(self.level, message)

    def flush(self):
        pass  # Not needed

class PyUiLogger:
    _logger = None  # Class-level cache for the logger

    @classmethod
    def init(cls, name="PyUiLogger"):
        if cls._logger is not None:
            return cls._logger

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)

            # File handler
            file_handler = logging.FileHandler("/mnt/SDCARD/Saves/spruce/pyui.log")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
            
        # Redirect stdout and stderr to logger
        sys.stdout = StreamToLogger(logger, logging.INFO)
        sys.stderr = StreamToLogger(logger, logging.ERROR)

        cls._logger = logger
        return cls._logger
    
    @classmethod
    def get_logger(cls, name="PyUiLogger"):
        return cls._logger
    
    
    @classmethod
    def info(cls, msg, name="PyUiLogger"):
        return cls._logger.info(msg)
    
    
    @classmethod
    def get_logger(cls, msg, name="PyUiLogger"):
        return cls._logger.error(msg)
    
    
    @classmethod
    def get_logger(cls, msg, name="PyUiLogger"):
        return cls._logger.debug(msg)
    
    
    @classmethod
    def get_logger(cls, msg, name="PyUiLogger"):
        return cls._logger.warning(msg)

