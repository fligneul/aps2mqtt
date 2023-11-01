"""Application config classes, can be set by file or env variable"""
import os
import yaml


class MQTTConfig:
    """MQTT config"""

    def __init__(self, cfg):
        self.broker_addr = cfg.get("MQTT_BROKER_HOST", "127.0.0.1")
        self.broker_port = cfg.get("MQTT_BROKER_PORT", 1883)
        self.broker_user = cfg.get("MQTT_BROKER_USER", "")
        self.broker_passwd = cfg.get("MQTT_BROKER_PASSWD", "")
        self.client_id = cfg.get("MQTT_CLIENT_ID", "APS2MQTT")
        self.topic_prefix = cfg.get("MQTT_TOPIC_PREFIX", "")


class ECUConfig:
    """ECU config"""

    def __init__(self, cfg):
        self.ipaddr = cfg["APS_ECU_IP"]
        self.port = cfg.get("APS_ECU_PORT", 8899)
        self.auto_restart = cfg.get("APS_ECU_AUTO_RESTART", False)
        if self.auto_restart:
            self.wifi_config = WifiConfig(
                cfg.get("APS_ECU_WIFI_SSID", ""), cfg.get("APS_ECU_WIFI_PASSWD", "")
            )
        self.stop_at_night = cfg.get("APS_ECU_STOP_AT_NIGHT", False)
        if self.stop_at_night:
            self.ecu_position_latitude = cfg.get("APS_ECU_POSITION_LAT", 48.864716)
            self.ecu_position_longitude = cfg.get("APS_ECU_POSITION_LNG", 2.349014)


class WifiConfig:
    """Wifi config of the ECU"""

    def __init__(self, ssid, passwd):
        self.ssid = ssid
        self.passwd = passwd


class Config:
    """Application config"""

    def __init__(self, config_path=None):
        if config_path is not None:
            with open(config_path, "r", encoding="UTF-8") as yml_cfg:
                cfg = yaml.safe_load(yml_cfg)
                self.mqtt_config = MQTTConfig(cfg["mqtt"])
                self.ecu_config = ECUConfig(cfg["ecu"])
        else:
            cfg = os.environ
            self.mqtt_config = MQTTConfig(cfg)
            self.ecu_config = ECUConfig(cfg)
