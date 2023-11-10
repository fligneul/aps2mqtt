"""Handle ECU requests"""
import logging
from datetime import datetime, timedelta, timezone
import requests
from suntime import Sun
from aps2mqtt.apsystems.APSystemsSocket import APSystemsSocket, APSystemsInvalidData

_LOGGER = logging.getLogger(__name__)


class ECU:
    def __init__(self, ecu_config):
        self.socket = APSystemsSocket(ecu_config.ipaddr)
        self.cached_data = {}
        self.ipaddr = ecu_config.ipaddr
        self.port = ecu_config.port
        self.retry = 5
        self.retry_count = 0
        self.querying = True
        self.ecu_restarting = False
        if ecu_config.auto_restart:
            self.wifi_config = ecu_config.wifi_config
        self.stop_at_night = ecu_config.stop_at_night
        if self.stop_at_night:
            self.ecu_location = Sun(
                ecu_config.ecu_position_latitude, ecu_config.ecu_position_longitude
            )

    def is_night(self):
        return (
            self.stop_at_night
            and (
                len(self.cached_data) > 0
                and self.cached_data.get("qty_of_online_inverters", 0) == 0
            )
            and (
                datetime.now(timezone.utc) < self.ecu_location.get_sunrise_time()
                or datetime.now(timezone.utc) > self.ecu_location.get_sunset_time()
            )
        )

    def wake_up_time(self):
        if self.ecu_location.get_sunrise_time() < datetime.now(timezone.utc):
            return self.ecu_location.get_sunrise_time(
                datetime.now(timezone.utc).date() + timedelta(days=1)
            )
        return self.ecu_location.get_sunrise_time()

    def invalid_data(self):
        # we got invalid data, increment retry counter
        self.retry_count += 1

        if self.retry_count == self.retry:
            _LOGGER.warning(
                "Communication with the ECU failed after %s repeated attempts.", self.retry
            )
            # Determine ECU type to decide ECU restart (for ECU-C and ECU-R with sunspec only)
            if (self.cached_data["ecu_id"][0:3] == "215") or (
                self.cached_data["ecu_id"][0:4] == "2162"
            ):
                data = {
                    "SSID": self.wifi_config.ssid,
                    "channel": 0,
                    "method": 2,
                    "psk_wep": "",
                    "psk_wpa": self.wifi_config.passwd,
                }
                _LOGGER.debug("Data sent with URL: %s", data)
                url = "http://" + str(self.ipaddr) + "/index.php/management/set_wlan_ap"
                headers = {"X-Requested-With": "XMLHttpRequest"}
                try:
                    get_url = requests.post(url, headers=headers, data=data, timeout=30)
                    _LOGGER.debug(
                        "Attempt to restart ECU gave as response: %s.", str(get_url.status_code)
                    )
                    self.ecu_restarting = True
                except IOError as err:
                    _LOGGER.warning(
                        "Attempt to restart ECU failed with error: %s. Querying is stopped automatically.",
                        err,
                    )
                    self.querying = False
            else:
                # Older ECU-R models starting with 2160
                _LOGGER.warning(
                    "Try manually power cycling the ECU. Querying is stopped automatically, turn switch back on after restart of ECU."
                )
                self.querying = False

        if self.cached_data["ecu_id"] is None:
            raise ValueError(
                "Unable to get correct data from ECU. See log for details, and try power cycling the ECU."
            )

    def update(self):
        _LOGGER.debug("Start ECU update")
        data = {}

        # if we aren't actively quering data.
        # this is so we can stop querying after sunset
        if not self.querying:
            _LOGGER.debug("Not querying ECU due to query=False")
            return data

        _LOGGER.debug("Querying ECU...")
        try:
            data = self.socket.query_ecu()
            _LOGGER.debug("Got data from ECU")

            # we got good results, so we store it and set flags about our
            # cache state
            if data["ecu_id"] is not None:
                self.cached_data = data
                self.ecu_restarting = False
            else:
                msg = "Error: no ecu_id returned"
                _LOGGER.warning(msg)
                data = {}

        except APSystemsInvalidData as err:
            msg = f"Invalid data error: {err}"
            if str(err) != "timed out":
                _LOGGER.warning(msg)
            data = {}

        except Exception as err:
            msg = f"Exception error: {err}"
            _LOGGER.warning(msg)
            data = {}

        if data.get("ecu_id", None) is None:
            self.cached_data = {}
            self.invalid_data()
            raise ValueError("Somehow data doesn't contain a valid ecu_id")

        data["querying"] = self.querying
        data["restart_ecu"] = self.ecu_restarting
        _LOGGER.debug("Returning %s", data)

        return data
