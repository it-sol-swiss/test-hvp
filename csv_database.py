# csv_database.py

import csv
import os


class CsvDatabase:
    logger = None
    path = None

    @classmethod
    def set_logger(cls, logger):
        cls.logger = logger

    def __init__(self, path=None):
        # Change the path to hv-bApp directory
        self.path = path or os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'hv-bApp',
                                         'database')
        os.makedirs(self.path, exist_ok=True)

        self.filename = os.path.join(self.path, "canbus_messages.csv")
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["timestamp", "id", "is_extended_id", "is_error_frame", "is_remote_frame", "dlc", "data"])

    def write_message(self, msg):
        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [msg.timestamp, msg.arbitration_id, msg.is_extended_id, msg.is_error_frame, msg.is_remote_frame,
                 msg.dlc,
                 msg.data])

        self.logger.info("Wrote message to database: %s", msg)
