import socket

from app.utils import logger as logger

log = logger.Logger()


class SchulzSocket:
    """
    This module provides mothods to connect, read and write to the Delta Elektronika PSU over Ethernet.
    """

    def __init__(self, ip='192.168.1.250', port=8462, timeout=10, watchdog=5000):
        # Setup connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        self.sock.connect((ip, port))
        self.sock.settimeout(None)

        # Clear messages
        message = '*CLS\r\n'
        self.sock.send(message.encode())
        # Reset unit
        message = '*RST\r\n'
        self.sock.send(message.encode())
        # Set Watchdog
        message = 'SYSTem:COMmunicate:WATchdog SET,' + str(watchdog) + '\r\n'
        self.sock.send(message.encode())

    def close_socket(self):
        """
        Closes socket
        """
        message = '*CLS\r\n'
        self.sock.send(message.encode())
        message = '*RST\r\n'
        self.sock.send(message.encode())
        self.sock.close()

    def read_error(self):
        """
        Read and clear error message
        """
        message = 'SYSTem:ERRor?\r\n'
        i = True
        while i:
            self.sock.send(message.encode())
            error = self.sock.recv(1024)
            log.log(error.decode('ascii'))
            if error == b'0,None\n':
                i = False

    def read_warning(self):
        """
        Read and clear warning message
        """
        message = 'SYSTem:WARning?\r\n'
        i = True
        while i:
            self.sock.send(message.encode())
            warning = self.sock.recv(1024)
            log.log(warning.decode('ascii'))
            if warning == b'0,None\n':
                i = False

    def feed_watchdog(self):
        """
        Feeds the dog to make him happy
        """
        message = 'SYSTem:COMmunicate:WATchdog?\r\n'
        self.sock.send(message.encode())
        answer = self.sock.recv(1024)

    def instrument(self, inst='Ah', op='OFF'):
        """
        Read and control integration instrument for Ah and Wh
        :param inst: 'Ah' or 'Wh' for Ampere-hour or Watt-hour instrument
        :param op: 'OFF', 'ON', 'SUSPEND', 'RESUME', 'READ_POS' or 'READ_NEG'
        :return:
        """
        message = []
        if inst == 'Ah':
            if op == 'READ_POS':
                message = 'MEASure:INStrument AH,POS,TOTAL?\r\n'
            elif op == 'READ_NEG':
                message = 'MEASure:INStrument AH,NEG,TOTAL?\r\n'
            else:
                message = 'MEASure:INStrument AH,STATE,' + op + '\r\n'

        elif inst == 'Wh':
            if op == 'READ_POS':
                message = 'MEASure:INStrument WH,POS,TOTAL?\r\n'
            elif op == 'READ_NEG':
                message = 'MEASure:INStrument WH,NEG,TOTAL?\r\n'
            else:
                message = 'MEASure:INStrument WH,STATE,' + op + '\r\n'

        self.sock.send(message.encode())

        if op == 'READ_POS' or op == 'READ_NEG':
            return float(self.sock.recv(1024).decode('ascii'))
        else:
            return None

    def set_output(self, state=False):
        """
        Set output to on (True) or off (False)
        """
        if state:
            state = 1
        else:
            state = 0
        message = 'OUTPut ' + str(state) + '\r\n'
        self.sock.send(message.encode())

    def get_voltage(self):
        """
        Read CV setting in [V]
        """
        message = 'SOURce:VOLtage?\r\n'
        self.sock.send(message.encode())
        return self.sock.recv(1024).decode('ascii')

    def set_voltage(self, u=0):
        """
        Set CV setting to given parameter in [V]
        """
        message = 'SOURce:VOLtage ' + str(u) + '\r\n'
        self.sock.send(message.encode())

    def measure_voltage(self):
        """
        Measures actual voltage at outlet in [V]
        """
        message = 'MEASure:VOLtage?\r\n'
        self.sock.send(message.encode())
        return float(self.sock.recv(1024).decode('ascii'))

    def get_current(self):
        """
        Read CC setting in [A]
        """
        message = 'SOURce:CURrent?\r\n'
        self.sock.send(message.encode())
        return self.sock.recv(1024).decode('ascii')

    def get_current_neg(self):
        """
        Read discharge CC setting in [A]
        """
        message = 'SOURce:CURrent:NEGative?\r\n'
        self.sock.send(message.encode())
        return self.sock.recv(1024).decode('ascii')

    def set_current(self, i=0):
        """
        Set CC setting to given parameter in [A]
        """
        i = min(i, 90)  # psu can only deliver 90 A
        message = ('SOURce:CURrent ' + str(i) + '\r\n')
        self.sock.send(message.encode())

    def set_current_neg(self, i=0):
        """
        Set discharge CC setting to given parameter in [A]
        """
        i = max(i, -90)  # psu can only drain 90 A
        message = ('SOURce:CURrent:NEGative ' + str(i) + '\r\n')
        self.sock.send(message.encode())

    def measure_current(self):
        """
        Measures actual current at outlet in [A]
        """
        message = 'MEASure:CURrent?\r\n'
        self.sock.send(message.encode())
        return float(self.sock.recv(1024).decode('ascii'))

    def get_power(self):
        """
        Read P setting in [W]
        """
        message = 'SOURce:POWer?<term>\r\n'
        self.sock.send(message.encode())
        return self.sock.recv(1024).decode('ascii')

    def get_power_neg(self):
        """
        Read discharge P setting in [W]
        """
        message = 'SOURce:POWer:NEGative?<term>\r\n'
        self.sock.send(message.encode())
        return self.sock.recv(1024).decode('ascii')

    def set_power(self, p=0):
        """
        Set P setting to given parameter in [W]
        """
        message = ('SOURce:POWer ' + str(p) + '\r\n')
        self.sock.send(message.encode())

    def set_power_neg(self, p=0):
        """
        Set discharge P setting to given parameter in [W]
        """
        message = ('SOURce:POWer:NEGative ' + str(p) + '\r\n')
        self.sock.send(message.encode())

    def measure_power(self):
        """
        Measures actual power at outlet in [W]
        """
        message = 'MEASure:POWer?\r\n'
        self.sock.send(message.encode())
        return float(self.sock.recv(1024).decode('ascii'))
