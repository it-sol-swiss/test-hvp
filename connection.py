# connection.py

import time
import threading
from can import Message
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from app.models.canbus.ixxat_interface import IxxatInterface
from app.utils.csv_database import CsvDatabase
from app.utils.logger_config import LoggerConfig

LOG_UPDATE_INTERVAL = 0.1  # Update log display every 100 ms


class Connection(Screen):
    ixxat = None
    database = None
    log_text = StringProperty('')  # Initialize log_text as an empty string
    receiver_thread = None

    @classmethod
    def set_ixxat(cls, ixxat: IxxatInterface):
        cls.ixxat = ixxat

    @classmethod
    def set_database(cls, database: CsvDatabase):
        cls.database = database

    def __init__(self, **kwargs):
        super(Connection, self).__init__(**kwargs)
        # Aktualisiere das Log alle LOG_UPDATE_INTERVAL Sekunden
        Clock.schedule_interval(self.update_log, LOG_UPDATE_INTERVAL)

    def update_log(self, *args):
        self.log_text = self.read_log()

    def read_log(self):
        while not LoggerConfig.filename:
            time.sleep(1)

        if LoggerConfig.filename:
            with open(LoggerConfig.filename, 'r') as f:
                return f.read()

    def on_log_text(self, instance, value):  # This method will be called whenever log_text changes
        self.ids.log_label.text = value  # Assuming you have a label with id "log_label" in your kv file

    def connect_ixxat(self):
        if self.ixxat:
            # Connect the Ixxat-Interface and start the receiving thread
            self.ixxat.connect()
            self.ixxat.set_filter({"can_id": 0x18FF50E5, "can_mask": 0x1FFFFFFF})
            return True
        return False

    def disconnect_ixxat(self):
        if self.ixxat:
            # Trenne das Ixxat-Interface
            self.ixxat.disconnect()
            return True
        return False

    def send_message(self, msg):
        if self.ixxat:
            self.ixxat.send(msg)

            if self.database:
                self.database.write_message(msg)

    def receive_message(self):
        if self.ixxat:
            msg = self.ixxat.receive()

            if msg and self.database:
                self.database.write_message(msg)

            return msg

    def receive_messages_forever(self):
        while True:
            msg = self.receive()
            if msg:
                self.logger.info("Received message: %s", msg)  # Zum Debuggen
                if self.database:
                    self.database.write_message(msg)

    def start_sniffing(self):
        if self.ixxat:
            # Start the receiving thread
            self.ixxat.connect()
            self.receiver_thread = threading.Thread(target=self.ixxat.receive_messages_forever, daemon=True)
            self.receiver_thread.start()
            return True
        return False

    def stop_sniffing(self):
        if self.ixxat and self.receiver_thread:
            # Stop the receiving thread
            self.ixxat.disconnect()
            return True
        return False

    def set_filter(self, filter):
        if self.ixxat:
            self.ixxat.set_filter(filter)

    def verify(self):
        msg = Message(arbitration_id=0x18FF50E5, data=[0, 0, 0, 0, 0, 0, 0, 0])
        self.send_message(msg)
