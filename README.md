[![Maintenance badge](https://img.shields.io/maintenance/yes/2025)](https://github.com/fligneul/aps2mqtt)
[![Release badge](https://img.shields.io/github/v/release/fligneul/aps2mqtt)](https://github.com/fligneul/aps2mqtt/releases)
[![PyPI version](https://badge.fury.io/py/aps2mqtt.svg)](https://badge.fury.io/py/aps2mqtt)
[![Docker Hub Badge](https://img.shields.io/badge/Docker_Hub-fligneul%2Faps2mqtt-blue?logo=docker&link=https%3A%2F%2Fhub.docker.com%2Fr%2Ffligneul%2Faps2mqtt)](https://hub.docker.com/r/fligneul/aps2mqtt)
[![Semantic release conventional](https://img.shields.io/badge/python_semantic_release-conventional-e10079?logo=semantic-release
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
| MQTT_RETAIN | Retain MQTT messages | True | False |
| MQTT_DISCOVERY_ENABLED | Enable MQTT discovery | True | False |
| MQTT_DISCOVERY_PREFIX | MQTT discovery prefix | "homeassistant" | "homeassistant" |
| MQTT_BROKER_SECURED_CONNECTION | Use secure connection to MQTT broker | True | False |
| MQTT_BROKER_CACERTS_PATH | Path to the cacerts file | "/User/johndoe/.ssl/cacerts" | None |

### ECU

| Key | Description | Example | Default value |
|---|---|---|---|
| APS_ECU_IP | IP of the ECU | "192.168.1.42" | None, this field id mandatory |
| APS_ECU_PORT | Communication port of the ECU | 8899 | 8899 |
| APS_ECU_TIMEZONE | Timezone of the ECU | 'Europe/Paris' | None (use system timezone) |
| APS_ECU_AUTO_RESTART | Automatically restart ECU in case of error | True | False |
| APS_ECU_WIFI_SSID | SSID of the ECU Wifi <br />:information_source: Only used if automatic restart is enabled | "My Wifi" | "" |
| APS_ECU_WIFI_PASSWD | Password of the ECU Wifi <br />:information_source: Only used if automatic restart is enabled | "secret-key" | "" |
| APS_ECU_STOP_AT_NIGHT | Stop ECU query during the night | True | False |
| APS_ECU_POSITION_LAT | Latitude of the ECU, used to retrieve sunset and sunrise <br />:information_source: Only used if stop at night is enabled | 51.49819 | 48.864716 (Paris) |
| APS_ECU_POSITION_LNG | Longitude of the ECU, used to retrieve sunset and sunrise <br />:information_source: Only used if stop at night is enabled | -0.13087 | 2.349014 (Paris) |

### Timezone

Without any specific configuration, aps2mqtt use your system's timezone as a reference.

* If you use aps2mqtt as a python application, setting the ECU timezone is recommended by setting the configuration variable 'APS_ECU_TIMEZONE' for better processing.  

* If you are using aps2mqtt as a Docker image, you can configure the timezone for the whole container using the environement variable 'TZ'

### MQTT Discovery

APS2MQTT supports MQTT discovery for seamless integration with home automation platforms like Home Assistant.

When enabled, `aps2mqtt` will publish configuration messages to the specified discovery prefix. These messages allow your home automation platform to automatically discover and configure the ECU and all its associated inverters and panels as devices and entities.

To enable this feature, set the `MQTT_DISCOVERY_ENABLED` option to `True` in your configuration.

```yaml
mqtt:
  # ... other mqtt settings
  MQTT_DISCOVERY_ENABLED: True
  # Optional: Change the discovery prefix if your platform requires it
  MQTT_DISCOVERY_PREFIX: 'homeassistant'
```

Once enabled, you should see the devices automatically appear in your home automation platform.

### Example

#### Unsecured connection

``` yaml
ecu:
  APS_ECU_IP: '192.168.1.42'
  APS_ECU_TIMEZONE: 'Europe/Paris'
  APS_ECU_STOP_AT_NIGHT: True
  APS_ECU_POSITION_LAT: 47.206
  APS_ECU_POSITION_LNG: -1.5645

mqtt:
  MQTT_BROKER_HOST: '192.168.1.12'
  MQTT_BROKER_PORT: 1883
  MQTT_BROKER_USER: 'johndoe'
  MQTT_BROKER_PASSWD: 'itsasecret'
  MQTT_RETAIN: True
  MQTT_DISCOVERY_ENABLED: True
```

#### Secured connection

``` yaml
ecu:
  APS_ECU_IP: '192.168.1.42'
  APS_ECU_TIMEZONE: 'Europe/Paris'
  APS_ECU_STOP_AT_NIGHT: True
  APS_ECU_POSITION_LAT: 47.206
  APS_ECU_POSITION_LNG: -1.5645

mqtt:
  MQTT_BROKER_HOST: 'broker.hivemq.com'
  MQTT_BROKER_PORT: 8883
  MQTT_BROKER_SECURED_CONNECTION: True
  MQTT_DISCOVERY_ENABLED: True
  MQTT_DISCOVERY_PREFIX: 'custom_discovery'
```

#### Using Docker Compose

``` yaml
services:
  aps2mqtt:
    image: fligneul/aps2mqtt:latest
    restart: always
    environment:
      - TZ=Europe/Paris
      - DEBUG=True
      - APS_ECU_IP=192.168.1.42
      - APS_ECU_STOP_AT_NIGHT=True
      - APS_ECU_POSITION_LAT=47.206
      - APS_ECU_POSITION_LNG=-1.5645
      - MQTT_BROKER_HOST=broker.hivemq.com
      - MQTT_BROKER_PORT=8883
      - MQTT_BROKER_USER=johndoe
      - MQTT_BROKER_PASSWD=itsasecret
      - MQTT_BROKER_SECURED_CONNECTION=True
```

## Breaking Changes

With the introduction of MQTT Discovery, the MQTT topic structure has changed significantly to align with Home Assistant's best practices for discovery. Previously, each data point was published to a separate topic (e.g., `aps/[ECU_ID]/power`). Now, data for an ECU or an inverter is published as a single JSON payload to a base topic (e.g., `aps/[ECU_ID]` or `aps/[ECU_ID]/[INVERTER_ID]`).

**Migration Steps:**

1.  **Enable MQTT Discovery:** It is highly recommended to enable MQTT Discovery by setting `MQTT_DISCOVERY_ENABLED: True` in your `mqtt` configuration. This will automatically configure your devices in Home Assistant.
2.  **Update Manual Configurations:** If you were previously using manual MQTT sensor configurations in Home Assistant (or any other platform), you will need to update them to reflect the new JSON payload structure and base topics. You will need to use `value_template` to extract the specific values from the JSON payload.

    **Example (Old vs. New for ECU Power):**

    **Old (Manual Sensor):**
    ```yaml
    mqtt:
      sensor:
        - name: "ECU Power"
          state_topic: "aps/123456789/power"
          unit_of_measurement: "W"
    ```

    **New (Manual Sensor - if not using discovery):**
    ```yaml
    mqtt:
      sensor:
        - name: "ECU Power"
          state_topic: "aps/123456789"
          unit_of_measurement: "W"
          value_template: "{{ value_json.current_power }}"
    ```

    Similar changes will be required for all inverter and panel sensors.

## MQTT topics

The `aps2mqtt` retrieves data from the entire PV array as a whole, as well as detailed information for each individual inverter.

*   `aps/status` - Current status of the `aps2mqtt` service, publishing `online` or `offline`. The `offline` message is sent as a Last Will and Testament (LWT) message by the MQTT broker upon unexpected disconnection. This topic is also used as the `availability_topic` for MQTT Discovery.

### ECU data

*   `aps/[ECU_ID]` - Publishes a JSON payload containing the following data for the entire ECU:
    *   `current_power` - Total amount of power (in W) being generated right now.
    *   `today_energy` - Total amount of energy (in kWh) generated today.
    *   `lifetime_energy` - Total amount of energy (in kWh) generated from the lifetime of the array.

### Inverter data

*   `aps/[ECU_ID]/[INVERTER_ID]` - Publishes a JSON payload containing the following data for each individual inverter:
    *   `online` - `True` if the inverter is communicating with the ECU, `False` otherwise.
    *   `signal` - The signal strength of the zigbee connection.
    *   `temperature` - The temperature of the inverter in your local unit (C or F).
    *   `frequency` - The AC power frequency (in Hz).
    *   `power` - The current power generation (in W), sum of all panel power.
    *   `voltage` - The AC voltage (in V).
    *   `panel_[ID]_power` - The current power generation (in W) of the selected panel.
    *   `panel_[ID]_voltage` - The AC voltage (in V) of the selected panel.