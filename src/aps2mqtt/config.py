"""Application config classes, can be set by file or env variable"""

import os
from dataclasses import dataclass, field
from zoneinfo import ZoneInfo

import yaml
from dateutil import tz
from str2bool import str2bool_exc


@dataclass
class MQTTDiscoveryConfig:
    """MQTT Discovery config"""

    prefix: str

    def __init__(self, cfg: dict) -> None:
        self.prefix = cfg.get("MQTT_DISCOVERY_PREFIX", "homeassistant")


@dataclass
class WifiConfig:
    """Wifi config of the ECU"""

    ssid: str
    passwd: str


@dataclass
class MQTTConfig:
    """MQTT config"""

    broker_addr: str = "127.0.0.1"
    broker_port: int = 1883
    broker_user: str = ""
    broker_passwd: str = ""
    client_id: str = "APS2MQTT"
    topic_prefix: str = ""
    retain: bool = False
    discovery_enabled: bool = False
    discovery: MQTTDiscoveryConfig | None = None
    secured_connection: bool = False
    cacerts_path: str | None = None

    def __init__(self, cfg: dict) -> None:
        self.broker_addr = cfg.get("MQTT_BROKER_HOST", "127.0.0.1")
        self.broker_port = int(cfg.get("MQTT_BROKER_PORT", 1883))
        self.broker_user = cfg.get("MQTT_BROKER_USER", "")
        self.broker_passwd = cfg.get("MQTT_BROKER_PASSWD", "")
        self.client_id = cfg.get("MQTT_CLIENT_ID", "APS2MQTT")
        self.topic_prefix = cfg.get("MQTT_TOPIC_PREFIX", "")
        self.retain = str2bool_exc(str(cfg.get("MQTT_RETAIN", False)))
        self.discovery_enabled = str2bool_exc(str(cfg.get("MQTT_DISCOVERY_ENABLED", False)))
        if self.discovery_enabled:
            self.discovery = MQTTDiscoveryConfig(cfg)
        self.secured_connection = str2bool_exc(
            str(cfg.get("MQTT_BROKER_SECURED_CONNECTION", False))
        )
        if self.secured_connection:
            self.cacerts_path = cfg.get("MQTT_BROKER_CACERTS_PATH")


@dataclass
class ECUConfig:
    """ECU config"""

    ipaddr: str = ""
    port: int = 8899
    timezone: ZoneInfo | tz.tzlocal = field(default_factory=tz.tzlocal)
    auto_restart: bool = False
    wifi_config: WifiConfig | None = None
    stop_at_night: bool = False
    ecu_position_latitude: float = 48.864716
    ecu_position_longitude: float = 2.349014

    def __init__(self, cfg: dict) -> None:
        self.ipaddr = cfg["APS_ECU_IP"]
        self.port = int(cfg.get("APS_ECU_PORT", 8899))
        ecu_timezone = cfg.get("APS_ECU_TIMEZONE", os.getenv("TZ", None))
        self.timezone = ZoneInfo(str(ecu_timezone)) if ecu_timezone is not None else tz.tzlocal()
        self.auto_restart = str2bool_exc(str(cfg.get("APS_ECU_AUTO_RESTART", False)))
        if self.auto_restart:
            self.wifi_config = WifiConfig(
                cfg.get("APS_ECU_WIFI_SSID", ""), cfg.get("APS_ECU_WIFI_PASSWD", "")
            )
        self.stop_at_night = str2bool_exc(str(cfg.get("APS_ECU_STOP_AT_NIGHT", False)))
        if self.stop_at_night:
            self.ecu_position_latitude = float(cfg.get("APS_ECU_POSITION_LAT", 48.864716))
            self.ecu_position_longitude = float(cfg.get("APS_ECU_POSITION_LNG", 2.349014))


class Config:
    """Application config"""

    mqtt_config: MQTTConfig
    ecu_config: ECUConfig

    def __init__(self, config_path: str | None = None) -> None:
        if config_path is not None:
            self._load_yaml_config_file(config_path)
        elif os.getenv("CONFIG_FILE") is not None:
            self._load_yaml_config_file(os.getenv("CONFIG_FILE"))
        else:
            cfg = os.environ
            self.mqtt_config = MQTTConfig(cfg)
            self.ecu_config = ECUConfig(cfg)

    def _load_yaml_config_file(self, config_path: str) -> None:
        with open(config_path, encoding="UTF-8") as yml_cfg:
            cfg = yaml.safe_load(yml_cfg)
            self.mqtt_config = MQTTConfig(cfg["mqtt"])
            self.ecu_config = ECUConfig(cfg["ecu"])
