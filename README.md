[![Maintenance badge](https://img.shields.io/maintenance/yes/2023)](https://github.com/fligneul/aps2mqtt)
[![Release badge](https://img.shields.io/github/v/release/fligneul/aps2mqtt)](https://github.com/fligneul/aps2mqtt/releases)
[![PyPI version](https://badge.fury.io/py/aps2mqtt.svg)](https://badge.fury.io/py/aps2mqtt)
[![Semantic release angular](https://img.shields.io/badge/python_semantic_release-angular-e10079?logo=semantic-release
)](https://github.com/python-semantic-release/python-semantic-release)

# APS2MQTT

Allows you to access your [APsystems](http://www.apsystems.com) Energy Communication Unit (ECU) data by MQTT. This MQTT bridge queries the ECU directly at regular interval for new data, parse the returned data and publish them over MQTT.

In this way you can integrate your APsystems devices with whatever smart home infrastructure you are using.

:warning: It currently supports only one ECU.

## Acknowledgements

This work is based on the awesome [homeassistant-apsystems_ecur (v1.2.30)](https://github.com/ksheumaker/homeassistant-apsystems_ecur). This couldn't have been done without their hardwork.

## Prerequisites

[See full version](aps2mqtt/apsystems/README.md#Prerequisites)

* A compatible APSystems ECU
  * ECU-B
  * ECU-R
  * ECU-C
* Some inverters
  * YC1000/QT2
  * YC600/DS3/DS3-H/DS3-L/DS3D
  * QS1/QS1A

Your ECU needs to be fully configured by the EMA Manager and should have a fixed IP address. APS2MQTT should run on a machine in the same network (or in an accessible one) as the ECU.

ECU-C and modern ECU-R (ID starting with 2162) can be automatically restarted in case of connection error. For older ECU-R and for ECU-B, the restart need to be done manually.

### Test your connection

[See full version](aps2mqtt/apsystems/README.md#Test-your-connection)

You can test the connection between APS2MQTT and the ECU using Netcat. From your terminal, run the following command (assuming your ECU IP address is 192.168.1.42) to open the connection

``` sh
nc -v 192.168.1.42 8899
```

ECU should response with an "open" message

``` sh
192.168.1.42 (192.168.1.42:8899) open
```

Connection is now established, the ECU is ready to receive commands

``` sh
APS1100160001END
```

If this command return with an APS message, you are ready to start APS2MQTT. If not, rebbot your ECU and try again.

## Install

Binaries are available in the release asset or on [PyPI](https://pypi.org/project/aps2mqtt/).
Using a virtual env is recommended for better insulation.

``` sh
# with PyPI
pip3 install aps2mqtt
# manually 
pip3 install aps2mqtt-[version]-py3-none-any.whl
```
Start it

``` sh
python3 -m aps2mqtt -h
```

### Run as a service

Using systemd, APS2MQTT can be started automatically

``` yaml
[Unit]
Description=APS2MQTT
After=multi-user.target

[Service]
Type=simple
User=user
Restart=on-failure
ExecStart=/path-to-your-venv/python3 -m aps2mqtt -c config.yaml

[Install]
WantedBy=multi-user.target
```

## Configuration

APS2MQTT configuration can be provided by a yaml config file or by environment variables (in a container context for example).

### MQTT

| Key | Description | Example | Default value |
|---|---|---|---|
| MQTT_BROKER_HOST | Host of the MQTT broker | "192.168.1.1", "broker.hivemq.com" | "127.0.0.1" |
| MQTT_BROKER_PORT | Port of the MQTT broker | 1883 | 1883 |
| MQTT_BROKER_USER | User login of the MQTT broker | "john-doe" | "" |
| MQTT_BROKER_PASSWD | User password of the MQTT broker | "itsasecret" | "" |
| MQTT_CLIENT_ID | Client ID if the MQTT client | "MyAwesomeClient" | "APS2MQTT" |
| MQTT_TOPIC_PREFIX | Topic prefix for publishing | "my-personal-topic" | "" |
| MQTT_BROKER_SECURED_CONNECTION | Use secure connection to MQTT broker | True | False |
| MQTT_BROKER_CACERTS_PATH | Path to the cacerts file | "/User/johndoe/.ssl/cacerts" | None |

### ECU

| Key | Description | Example | Default value |
|---|---|---|---|
| APS_ECU_IP | IP of the ECU | "192.168.1.42" | None, this field id mandatory |
| APS_ECU_PORT | Communication port of the ECU | 8899 | 8899 |
| APS_ECU_AUTO_RESTART | Automatically restart ECU in case of error | True | False |
| APS_ECU_WIFI_SSID | SSID of the ECU Wifi <br />:information_source: Only used if automatic restart is enabled | "My Wifi" | "" |
| APS_ECU_WIFI_PASSWD | Password of the ECU Wifi <br />:information_source: Only used if automatic restart is enabled | "secret-key" | "" |
| APS_ECU_STOP_AT_NIGHT | Stop ECU query during the night | True | False |
| APS_ECU_POSITION_LAT | Latitude of the ECU, used to retrieve sunset and sunrise <br />:information_source: Only used if stop at night is enabled | 51.49819 | 48.864716 (Paris) |
| APS_ECU_POSITION_LNG | Longitude of the ECU, used to retrieve sunset and sunrise <br />:information_source: Only used if stop at night is enabled | -0.13087 | 2.349014 (Paris) |

### Example

#### Unsecured connection

``` yaml
ecu:
  APS_ECU_IP: '192.168.1.42'
  APS_ECU_STOP_AT_NIGHT: True
  APS_ECU_POSITION_LAT: 47.206
  APS_ECU_POSITION_LNG: -1.5645

mqtt:
  MQTT_BROKER_HOST: '192.168.1.12'
  MQTT_BROKER_PORT: 1883
  MQTT_BROKER_USER: 'johndoe'
  MQTT_BROKER_PASSWD: 'itsasecret'
```

#### Secured connection

``` yaml
ecu:
  APS_ECU_IP: '192.168.1.42'
  APS_ECU_STOP_AT_NIGHT: True
  APS_ECU_POSITION_LAT: 47.206
  APS_ECU_POSITION_LNG: -1.5645

mqtt:
  MQTT_BROKER_HOST: 'broker.hivemq.com'
  MQTT_BROKER_PORT: 8883
  MQTT_BROKER_SECURED_CONNECTION: True

```

## MQTT topics

The aps2mqtt retrieve from the whole PV array as a whole as well as each individual inverter in detail.

### ECU data

* aps/[ECU_ID]/power - total amount of power (in W) being generated right now
* aps/[ECU_ID]/energy/today - total amount of energy (in kWh) generated today
* aps/[ECU_ID]/energy/lifetime - total amount of energy (in kWh) generated from the lifetime of the array

### Inverter data

* aps/[ECU_ID]/[INVERTER_ID]/online - True is the inverter is communicating with the ECU, False otherwise
* aps/[ECU_ID]/[INVERTER_ID]/signal - the signal strength of the zigbee connection
* aps/[ECU_ID]/[INVERTER_ID]/temperature - the temperature of the inverter in your local unit (C or F)
* aps/[ECU_ID]/[INVERTER_ID]/frequency - the AC power frequency (in Hz)
* aps/[ECU_ID]/[INVERTER_ID]/power - the current power generation (in W), sum of all panel power
* aps/[ECU_ID]/[INVERTER_ID]/voltage - the AC voltage (in V)
* aps/[ECU_ID]/[INVERTER_ID]/[PANEL_ID]/power - the current power generation (in W) of the selected panel
