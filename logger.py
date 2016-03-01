import time
from datetime import datetime
import config

def nowtime():
    timestamp = time.time()
    datetimestamp = datetime.fromtimestamp(timestamp)
    return datetimestamp.strftime(config.log_time_format_string)

def info(message):
    write("[INFO]\t" + nowtime() + ": " + message)

def debug(message):
    write("[DEBUG]\t" + nowtime() + ": " + message)

def error(message):
    write("![ERR]!\t" + nowtime() + ": " + message)

def write(message):
    if config.log_to_console:
        print(message)
    if config.log_to_file:
        file = open(config.log_file_path, 'a');
        file.write(message + '\n');
