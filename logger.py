import config

def write(message):
    if config.log_to_console:
        print(message)
    if config.log_to_file:
        file = open(config.log_file_path, 'a');
        file.write(message + '\n');
