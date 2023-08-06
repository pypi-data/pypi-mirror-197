import google.cloud.logging
import logging

def init(print2log=False):
    if not print2log:
        client = google.cloud.logging.Client()
        client.setup_logging()

def box_log(msg, level='info', print2log=False):
    levels = {
        'info': logging.info,
        'debug': logging.debug,
        'warning': logging.warning,
        'error': logging.error,
        'critical': logging.critical
    }
    if print2log:
        log = levels[level]
        log(msg)
    else:
        print(f'{level}: {msg}')