"""Open communication socket to APSystems ECU, send requests and parse received data"""
import socket
import binascii
import datetime
import logging
import time

_LOGGER = logging.getLogger(__name__)


class APSystemsInvalidData(Exception):
    pass


class APSystemsInvalidInverter(Exception):
    pass


class APSystemsSocket:
    def __init__(self, ipaddr, port=8899, raw_ecu=None, raw_inverter=None):
        self.ipaddr = ipaddr
        self.port = port

        # what do we expect socket data to end in
        self.recv_suffix = b"END\n"

        # how long to wait on socket commands until we get our recv_suffix
        self.timeout = 10

        # how big of a buffer to read at a time from the socket
        # https://github.com/ksheumaker/homeassistant-apsystems_ecur/issues/108
        self.recv_size = 1024

        # how long to wait between socket open/closes
        self.socket_sleep_time = 5

        self.cmd_suffix = "END\n"
        self.ecu_query = "APS1100160001" + self.cmd_suffix
        self.inverter_query_prefix = "APS1100280002"
        self.inverter_query_suffix = self.cmd_suffix
        self.inverter_signal_prefix = "APS1100280030"
        self.inverter_signal_suffix = self.cmd_suffix
        self.inverter_byte_start = 26
        self.ecu_id = None
        self.qty_of_inverters = 0
        self.qty_of_online_inverters = 0
        self.lifetime_energy = 0
        self.current_power = 0
        self.today_energy = 0
        self.inverters = []
        self.firmware = None
        self.timezone = None
        self.last_update = None
        self.vsl = 0
        self.tsl = 0
        self.ecu_raw_data = raw_ecu
        self.inverter_raw_data = raw_inverter
        self.inverter_raw_signal = None
        self.read_buffer = b""
        self.reader = None
        self.writer = None
        self.socket = None
        self.socket_open = False
        self.errors = []

    def send_read_from_socket(self, cmd):
        try:
            self.sock.settimeout(self.timeout)
            self.sock.sendall(cmd.encode("utf-8"))
            time.sleep(self.socket_sleep_time)
            self.read_buffer = b""
            self.sock.settimeout(self.timeout)
            # An infinite loop was causing the integration to block
            # https://github.com/ksheumaker/homeassistant-apsystems_ecur/issues/115
            # Solution might cause a new issue when large solar array's applies
            self.read_buffer = self.sock.recv(self.recv_size)
            return self.read_buffer
        except Exception as err:
            self.close_socket()
            raise APSystemsInvalidData(err)

    def close_socket(self):
        try:
            if self.socket_open:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.settimeout(self.timeout)
                data = self.sock.recv(
                    self.recv_size
                )  # flush incoming/outgoing data after shutdown request before actually closing the socket
                self.sock.close()
                self.socket_open = False
        except Exception as err:
            raise APSystemsInvalidData(err)

    def open_socket(self):
        self.socket_open = False
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.ipaddr, self.port))
            self.socket_open = True
        except Exception as err:
            raise APSystemsInvalidData(err)

    def query_ecu(self):
        self.open_socket()
        cmd = self.ecu_query
        self.ecu_raw_data = self.send_read_from_socket(cmd)
        self.close_socket()
        try:
            self.process_ecu_data()
            # conflicting interests of which 113 is just a temorary issue and less common
            # https://github.com/ksheumaker/homeassistant-apsystems_ecur/issues/126
            # https://github.com/ksheumaker/homeassistant-apsystems_ecur/issues/113
            if self.lifetime_energy == 0:
                error = f"ECU returned 0 for lifetime energy, this is either a glitch from the ECU or a brand new installed ECU. Raw Data={self.ecu_raw_data}"
                self.add_error(error)
                raise APSystemsInvalidData(error)
        except Exception as err:
            raise APSystemsInvalidData(err)

        # Some ECUs likes the socket to be closed and re-opened between commands
        self.open_socket()
        cmd = self.inverter_query_prefix + self.ecu_id + self.inverter_query_suffix
        self.inverter_raw_data = self.send_read_from_socket(cmd)
        self.close_socket()

        # Some ECUs likes the socket to be closed and re-opened between commands
        self.open_socket()
        cmd = self.inverter_signal_prefix + self.ecu_id + self.inverter_signal_suffix
        self.inverter_raw_signal = self.send_read_from_socket(cmd)

        self.close_socket()

        data = self.process_inverter_data()
        data["ecu_id"] = self.ecu_id
        data["today_energy"] = self.today_energy
        data["lifetime_energy"] = self.lifetime_energy
        data["current_power"] = self.current_power
        data["qty_of_inverters"] = self.qty_of_inverters
        data["qty_of_online_inverters"] = self.qty_of_online_inverters
        return data

    def aps_int(self, codec, start):
        try:
            return int(binascii.b2a_hex(codec[(start) : (start + 2)]), 16)
        except ValueError as err:
            debugdata = binascii.b2a_hex(codec)
            error = f"Unable to convert binary to int location={start} data={debugdata}"
            self.add_error(error)
            raise APSystemsInvalidData(error)

    def aps_short(self, codec, start):
        try:
            return int(binascii.b2a_hex(codec[(start) : (start + 1)]), 8)
        except ValueError as err:
            debugdata = binascii.b2a_hex(codec)
            error = f"Unable to convert binary to short int location={start} data={debugdata}"
            self.add_error(error)
            raise APSystemsInvalidData(error)

    def aps_double(self, codec, start):
        try:
            return int(binascii.b2a_hex(codec[(start) : (start + 4)]), 16)
        except ValueError as err:
            debugdata = binascii.b2a_hex(codec)
            error = f"Unable to convert binary to double location={start} data={debugdata}"
            self.add_error(error)
            raise APSystemsInvalidData(error)

    def aps_bool(self, codec, start):
        return bool(binascii.b2a_hex(codec[(start) : (start + 2)]))

    def aps_uid(self, codec, start):
        return str(binascii.b2a_hex(codec[(start) : (start + 12)]))[2:14]

    def aps_str(self, codec, start, amount):
        return str(codec[start : (start + amount)])[2 : (amount + 2)]

    def aps_timestamp(self, codec, start, amount):
        timestr = str(binascii.b2a_hex(codec[start : (start + amount)]))[2 : (amount + 2)]
        return (
            timestr[0:4]
            + "-"
            + timestr[4:6]
            + "-"
            + timestr[6:8]
            + " "
            + timestr[8:10]
            + ":"
            + timestr[10:12]
            + ":"
            + timestr[12:14]
        )

    def check_ecu_checksum(self, data, cmd):
        datalen = len(data) - 1
        try:
            checksum = int(data[5:9])
        except ValueError as err:
            debugdata = binascii.b2a_hex(data)
            error = f"could not extract checksum int from '{cmd}' data={debugdata}"
            self.add_error(error)
            raise APSystemsInvalidData(error)

        if datalen != checksum:
            debugdata = binascii.b2a_hex(data)
            error = (
                f"Checksum on '{cmd}' failed checksum={checksum} datalen={datalen} data={debugdata}"
            )
            self.add_error(error)
            raise APSystemsInvalidData(error)

        start_str = self.aps_str(data, 0, 3)
        end_str = self.aps_str(data, len(data) - 4, 3)

        if start_str != "APS":
            debugdata = binascii.b2a_hex(data)
            error = (
                f"Result on '{cmd}' incorrect start signature '{start_str}' != APS data={debugdata}"
            )
            self.add_error(error)
            raise APSystemsInvalidData(error)

        if end_str != "END":
            debugdata = binascii.b2a_hex(data)
            error = f"Result on '{cmd}' incorrect end signature '{end_str}' != END data={debugdata}"
            self.add_error(error)
            raise APSystemsInvalidData(error)

        return True

    def process_ecu_data(self, data=None):
        if self.ecu_raw_data != "" and (self.aps_str(self.ecu_raw_data, 9, 4)) == "0001":
            data = self.ecu_raw_data
            _LOGGER.debug(binascii.b2a_hex(data))
            self.check_ecu_checksum(data, "ECU Query")
            self.ecu_id = self.aps_str(data, 13, 12)
            self.lifetime_energy = self.aps_double(data, 27) / 10
            self.current_power = self.aps_double(data, 31)
            self.today_energy = self.aps_double(data, 35) / 100
            if self.aps_str(data, 25, 2) == "01":
                self.qty_of_inverters = self.aps_int(data, 46)
                self.qty_of_online_inverters = self.aps_int(data, 48)
                self.vsl = int(self.aps_str(data, 52, 3))
                self.firmware = self.aps_str(data, 55, self.vsl)
                self.tsl = int(self.aps_str(data, 55 + self.vsl, 3))
                self.timezone = self.aps_str(data, 58 + self.vsl, self.tsl)
            elif self.aps_str(data, 25, 2) == "02":
                self.qty_of_inverters = self.aps_int(data, 39)
                self.qty_of_online_inverters = self.aps_int(data, 41)
                self.vsl = int(self.aps_str(data, 49, 3))
                self.firmware = self.aps_str(data, 52, self.vsl)

    def process_signal_data(self, data=None):
        signal_data = {}
        if (
            self.inverter_raw_signal != ""
            and (self.aps_str(self.inverter_raw_signal, 9, 4)) == "0030"
        ):
            data = self.inverter_raw_signal
            _LOGGER.debug(binascii.b2a_hex(data))
            self.check_ecu_checksum(data, "Signal Query")
            if not self.qty_of_inverters:
                return signal_data
            location = 15
            for i in range(0, self.qty_of_inverters):
                uid = self.aps_uid(data, location)
                location += 6
                strength = data[location]
                location += 1
                strength = int((strength / 255) * 100)
                signal_data[uid] = strength
            return signal_data

    def process_inverter_data(self, data=None):
        output = {}
        if self.inverter_raw_data != "" and (self.aps_str(self.inverter_raw_data, 9, 4)) == "0002":
            data = self.inverter_raw_data
            _LOGGER.debug(binascii.b2a_hex(data))
            self.check_ecu_checksum(data, "Inverter data")
            istr = ""
            cnt1 = 0
            cnt2 = 26
            if self.aps_str(data, 14, 2) == "00":
                timestamp = self.aps_timestamp(data, 19, 14)
                inverter_qty = self.aps_int(data, 17)
                self.last_update = timestamp
                output["timestamp"] = timestamp
                output["inverters"] = []
                signal = self.process_signal_data()
                inverters = []

                while cnt1 < inverter_qty:
                    inv = {}
                    if self.aps_str(data, 15, 2) == "01":
                        inverter_uid = self.aps_uid(data, cnt2)
                        inv["uid"] = inverter_uid
                        inv["online"] = bool(self.aps_short(data, cnt2 + 6))
                        istr = self.aps_str(data, cnt2 + 7, 2)
                        inv["signal"] = signal.get(inverter_uid, 0)
                        if istr in [ '01', '04', '05']:
                            power = []
                            voltages = []
                            inv["frequency"] = self.aps_int(data, cnt2 + 9) / 10
                            if inv["online"]:
                                inv["temperature"] = self.aps_int(data, cnt2 + 11) - 100
                            power.append(self.aps_int(data, cnt2 + 13))
                            voltages.append(self.aps_int(data, cnt2 + 15))
                            power.append(self.aps_int(data, cnt2 + 17))
                            voltages.append(self.aps_int(data, cnt2 + 19))
                            inv_desc = {
                                "model": "YC600/DS3D/DS3-H/DS3/DS3-L",
                                "channel_qty": 2,
                                "power": power,
                                "voltage": voltages,
                            }
                            inv.update(inv_desc)
                            cnt2 = cnt2 + 21
                        elif istr == "02":
                            power = []
                            voltages = []
                            inv["frequency"] = self.aps_int(data, cnt2 + 9) / 10
                            if inv["online"]:
                                inv["temperature"] = self.aps_int(data, cnt2 + 11) - 100
                            power.append(self.aps_int(data, cnt2 + 13))
                            voltages.append(self.aps_int(data, cnt2 + 15))
                            power.append(self.aps_int(data, cnt2 + 17))
                            voltages.append(self.aps_int(data, cnt2 + 19))
                            power.append(self.aps_int(data, cnt2 + 21))
                            voltages.append(self.aps_int(data, cnt2 + 23))
                            power.append(self.aps_int(data, cnt2 + 25))
                            inv_desc = {
                                "model": "YC1000/QT2",
                                "channel_qty": 4,
                                "power": power,
                                "voltage": voltages,
                            }
                            inv.update(inv_desc)
                            cnt2 = cnt2 + 27
                        elif istr == "03":
                            power = []
                            voltages = []
                            inv["frequency"] = self.aps_int(data, cnt2 + 9) / 10
                            if inv["online"]:
                                inv["temperature"] = self.aps_int(data, cnt2 + 11) - 100
                            power.append(self.aps_int(data, cnt2 + 13))
                            voltages.append(self.aps_int(data, cnt2 + 15))
                            power.append(self.aps_int(data, cnt2 + 17))
                            power.append(self.aps_int(data, cnt2 + 19))
                            power.append(self.aps_int(data, cnt2 + 21))
                            inv_desc = {
                                "model": "QS1",
                                "channel_qty": 4,
                                "power": power,
                                "voltage": voltages,
                            }
                            inv.update(inv_desc)
                            cnt2 = cnt2 + 23
                        else:
                            cnt2 = cnt2 + 9
                        inverters.append(inv)
                    cnt1 = cnt1 + 1
                self.inverters = inverters
                output["inverters"] = inverters
                return output

    def add_error(self, error):
        timestamp = datetime.datetime.now()
        self.errors.append(f"[{timestamp}] {error}")
