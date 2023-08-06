# import google.cloud.logging
# import logging

# class Log:
#     def __init__(self, print=False):
#         self.print = print
#         client = google.cloud.logging.Client()
#         client.setup_logging()
            

#     def p(self, msg, level='info'):
#         levels = {
#             'info': logging.info,
#             'debug': logging.debug,
#             'warning': logging.warning,
#             'error': logging.error,
#             'critical': logging.critical
#         }
#         level = 'info' if level not in levels else level
#         if self.print:
#             print(f'{level.upper()}: {msg}')
#         else:
#             log = levels[level]
#             log(msg)