import os.path
import logging
from logging.handlers import TimedRotatingFileHandler

from config import BASE_DIR, APP_LOGGER_NAME

log_file_name = "currency.log"
log_dir_name = "log"
handler_suffix_pattern = "%d-%m-%Y"
log_file_path = os.path.join(BASE_DIR, os.path.join(log_dir_name, log_file_name))
f_format = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(filename)s %(funcName)s %(message)s',
                             datefmt="%d.%m.%Y %H:%M:%S")

f_handler = TimedRotatingFileHandler(filename=log_file_path, when="midnight", interval=1, encoding="utf-8")
f_handler.suffix = handler_suffix_pattern
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(f_format)

app_logger = logging.getLogger(APP_LOGGER_NAME)
app_logger.addHandler(f_handler)
app_logger.level = logging.DEBUG


