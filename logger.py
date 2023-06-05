from datetime import datetime


class Logger:
    """
    This module provides simple methods to create and append data to a log file.
    """

    def __init__(self):  # do something... ??
        f = open("log.txt", "a+")
        f.close()

    @staticmethod
    def start():
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        f = open("log.txt", "a+")
        f.write("\n\n" + current_time + ": New log\n")
        f.close()

    @staticmethod
    def log(message, do_print=1):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        f = open("log.txt", "a+")
        f.write(current_time + ": " + message + "\n")
        f.close()
        if do_print:
            print(current_time + ": " + message)
