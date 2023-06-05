# main.py

import os
import time

from app.models.canbus.ixxat_interface import IxxatInterface
from app.utils.csv_database import CsvDatabase
from app.utils.logger_config import configure_logger, LoggerConfig
from app.controllers.connection import Connection
from app.view.hvbapp import HvBApp

"""
os.system(
    'echo "admin" | sudo -S ip link add can0 up type can bitrate 250000')
"""


def main():
    # Create the logger here
    logger = configure_logger(terminal_output=True)
    # Create the database
    database = CsvDatabase()

    logger.info("Start")

    # Pass it to the IxxatInterface and CsvDatabase classes
    IxxatInterface.set_logger(logger)
    IxxatInterface.set_database(database)
    CsvDatabase.set_logger(logger)

    Connection.set_ixxat(IxxatInterface())
    Connection.set_database(database)

    # Ensure that the logger and database are setup before running the app
    while LoggerConfig.filename is None or not os.path.exists(LoggerConfig.filename):
        time.sleep(1)  # Wait for the logger and the database to be setup

    HvBApp().run()

    logger.info("End")


if __name__ == "__main__":
    main()
