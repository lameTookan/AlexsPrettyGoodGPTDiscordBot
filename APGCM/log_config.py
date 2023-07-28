import logging 

from pathlib import Path
from settings import DEFAULT_LOGGING_LEVEL, DEFAULT_LOGGING_DIR


DEFAULT_LOGGING_LEVEL = DEFAULT_LOGGING_LEVEL
LOGGING_FORMAT = '[%(asctime)s] %(name)s - %(levelname)s #%(lineno)s :: %(message)s'
LOGGING_FILE_PATH = DEFAULT_LOGGING_DIR


"""
Simple logging setup for the project.

"""
class BaseLogger:
    def __init__(self, module_name: str, filename: str = "pretty_good_log.log",  identifier: str = "Pretty Good Logger",  level: int = DEFAULT_LOGGING_LEVEL, format: str = LOGGING_FORMAT, file_path: str = LOGGING_FILE_PATH):
        self.name = module_name
        self.filename = filename
        self.identifier = identifier
        self.level = level
        self.format = identifier + "||" + format
        self.file_path = file_path
        self._logger = self._setup_logger()
    def _setup_logger(self) -> logging.Logger:
        """Setup the logger for the project. Also creates logging file and directory if it doesn't exist."""
        logger = logging.getLogger(self.name)
        path_folder = Path("./" +self.file_path)
        #print(str(path_folder))
        if not path_folder.exists():
            path_folder.mkdir(parents=True, exist_ok=True)
    
        path = path_folder / self.filename
        path.with_suffix(".log")
     
        path.touch(exist_ok=True)
        logger.setLevel(self.level)
        self.file_handler = logging.FileHandler(str(path))
        self.file_handler.setLevel(self.level)
        self.file_handler.setFormatter(logging.Formatter(self.format))
        logger.addHandler(self.file_handler)
        return logger
    @property
    def logger(self):
        """Return the logger."""
        return self._logger
    @logger.setter
    def logger(self, logger: logging.Logger):
        """Set the logger."""
        self._logger = logger
    def set_logging_level(self, level: int):
        """Set the logging level."""
        self._logger.setLevel(level)
    @property 
    def logging_level(self)-> int:
        """Return the logging level."""
        return self._logger.level
    @logging_level.setter
    def logging_level(self, level: int):
        """Set the logging level."""
        self.set_logging_level(level)
    def set_logging_format(self, format: str):
        """Set the logging format."""
        self.file_handler.setFormatter(logging.Formatter(self.identifier + format))
        self.format = format
        self._logger.removeHandler(self._logger.handlers[0])
        self._logger.addHandler(self.file_handler)
    def set_logging_file_path(self, file_path: str):
        """Set the logging file path."""
        self._logger.removeHandler(self._logger.handlers[0])
        self.file_path = file_path
        self._setup_logger()
  
    def add_handler(self, handler: logging.Handler):
        """Set the logging file path."""
        if not isinstance(handler, logging.Handler):
            raise TypeError("Handler must be of type logging.Handler")
        self._logger.addHandler(handler)
    #====(WRAPPERS FOR LOGGING METHODS)====
    # for convenience
    def debug(self, msg, *args, **kwargs):

        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self._logger.exception(msg, *args, **kwargs)
    
    def log(self, level, msg, *args, **kwargs):
        self._logger.log(level, msg, *args, **kwargs)