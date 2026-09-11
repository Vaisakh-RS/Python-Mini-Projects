import logging

def setup_logging():
    root_logger = logging.getLogger()   # no name passed = root logger
    root_logger.setLevel(logging.DEBUG)
    #print to the console and to a log file
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("app.log", mode="w")

    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    console_handler.setFormatter(log_formatter)
    file_handler.setFormatter(log_formatter)

    # 4. Bind handlers to your logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
