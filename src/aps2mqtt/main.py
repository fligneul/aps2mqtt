"""Query APS ECU data periodically and send them to the MQTT broker"""

import logging
import os
import time

from argparse import ArgumentParser
from datetime import datetime, timedelta, timezone
from str2bool import str2bool_exc
from aps2mqtt.mqtthandler import MQTTHandler
from aps2mqtt.config import Config
from aps2mqtt.apsystems.ECU import ECU

_LOGGER = logging.getLogger(__name__)


def cli_args():
    """Create CLI arguments and parse them"""
    parser = ArgumentParser(prog="aps2mqtt")
    parser.add_argument(
        "-c", "--config", dest="config_path", help="load YAML config file", metavar="FILE"
    )
    parser.add_argument(
        "-D", "--debug", dest="debug_level", help="enable debug logs", action="store_true"
    )

    return parser.parse_args()


def main():
    """Application main"""
    update_time = datetime(1970, 1, 1).astimezone()

    args = cli_args()
    conf = Config(args.config_path)

    if args.debug_level or str2bool_exc(os.getenv("DEBUG", "False")):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    ecu = ECU(conf.ecu_config)
    mqtt_handler = MQTTHandler(conf.mqtt_config)
    mqtt_handler.connect_mqtt()

    while 1:
        if datetime.now().astimezone() > update_time:
            if ecu.is_night():
                update_time = ecu.wake_up_time()
                _LOGGER.info(
                    "Time to sleep, next update at: %s",
                    update_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
                )
            else:
                try:
                    data = ecu.update()
                    if data is None or len(data) == 0:
                        raise ValueError("Retrieved data are empty")
                    update_time = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S").replace(
                        tzinfo=conf.ecu_config.timezone
                    ).astimezone() + timedelta(seconds=360)
                    mqtt_handler.publish_values(data)
                except Exception as e:
                    update_time = datetime.now().astimezone() + timedelta(seconds=60)
                    _LOGGER.error("An exception occured: %s -> %s", e.__class__.__name__, str(e))
                    _LOGGER.debug("Exception trace:", exc_info=True)
                _LOGGER.info(
                    "Update finished, next update at: %s",
                    update_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
                )

        time.sleep(5)


if __name__ == "__main__":
    main()
