# MicroPython BME280/BMP280 ESP32 MQTT Sensor

This is a simple MicroPython script for ESP32 that reads data from a BME280/BMP280 sensor and publishes it to an MQTT broker. The script also includes functionality to handle Wi-Fi connectivity, MQTT communication, and periodic sensor readings.

## Prerequisites

Make sure you have the following libraries installed on your ESP32:

- `umqtt.simple`
- `machine`
- `bme280`
- `utime`
- `ntptime`
- `ujson`
- `time`

## Setup

1. **Install MicroPython on ESP32**: Ensure that MicroPython is installed on your ESP32 device.

2. **Wiring**: Connect your BME280/BMP280 sensor to the ESP32 using the specified SDA and SCL pins.

3. **Configure `config.json`**: Create a file named `config.json` with the following structure:

    ```json
    {
        "name": "your_node_name",
        "ssid": "your_wifi_ssid",
        "pass": "your_wifi_password",
        "broker": "mqtt_broker_address",
        "sda_pin": your_sda_pin,
        "scl_pin": your_scl_pin,
        "period": sensor_read_interval_seconds
    }
    ```

## Usage

1. Upload the script and `config.json` to your ESP32 device.

2. Run the script on your ESP32. It will connect to the specified Wi-Fi network, initialize the BME280/BMP280 sensor, and start publishing sensor data to the MQTT broker.

3. Monitor the sensor data by subscribing to the following MQTT topics:
   - `<node_name>/status`: Online/Offline status of the ESP32 node.
   - `<node_name>/sens`: Sensor data in JSON format (`{"temp": temperature, "hum": humidity, "press": pressure}`).

4. Optionally, you can control a relay connected to your ESP32 by publishing messages to the topic `<node_name>/relay/set`.

## Troubleshooting

If you encounter issues, check the following:

- Ensure the correct wiring of the BME280/BMP280 sensor.
- Verify that the `config.json` file is properly configured.
- Check the Wi-Fi connection details.
- Monitor the console for any error messages.

## Acknowledgments

This script utilizes the `umqtt.simple` library for MQTT communication and the `bme280` library for interfacing with the BME280/BMP280 sensor.

## TODO

- [ ] Add support for additional features.
- [ ] Implement error handling for different scenarios.

## References

- [MicroPython BMP280 Library](https://github.com/dafvid/micropython-bmp280)
- [MicroPython I2C Documentation](https://docs.micropython.org/en/latest/library/machine.I2C.html)
