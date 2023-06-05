# ixxat_interface.py

import can
import threading

from app.utils.csv_database import CsvDatabase

class IxxatInterface:
    _instance = None
    logger = None
    database = None

    @classmethod
    def set_logger(cls, logger):
        cls.logger = logger

    @classmethod
    def set_database(cls, database: CsvDatabase):
        cls.database = database
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(IxxatInterface, cls).__new__(cls, *args, **kwargs)
            cls._instance._init(*args, **kwargs)
        return cls._instance

    def _init(self, channel="can0", bitrate=250000):
        self.channel = channel
        self.bitrate = bitrate
        self.bus = None

    def connect(self):
        if not self.bus:
            try:
                self.bus = can.interface.Bus(bustype='socketcan', channel=self.channel, bitrate=self.bitrate)
                self.stop_event = threading.Event()
                self.logger.info("Successfully connected to SocketCAN interface")
            except Exception as e:
                self.logger.error("Error: %s", e)

    def disconnect(self):
        if self.bus:
            self.stop_event.set()
            self.bus.shutdown()
            self.bus = None
            self.logger.info("Disconnected from SocketCAN interface")

    def send(self, msg):
        if self.bus:
            self.bus.send(msg)
        else:
            self.logger.warning("Not connected")

    def receive(self, timeout=1.0):
        if self.bus:
            return self.bus.recv(timeout)
        else:
            self.logger.warning("Not connected")
            return None

    def receive_messages_forever(self):
        while not self.stop_event.is_set():
            msg = self.receive()
            if msg:
                self.logger.info("Received message: %s", msg)
                if self.database:
                    self.database.write_message(msg)
    def set_filter(self, filter):
        if self.bus:
            self.bus.set_filters([filter])
            self.logger.info("Filter set: %s", filter)