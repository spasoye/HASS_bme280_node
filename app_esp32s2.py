from umqtt.simple import MQTTClient
import machine
from bme280 import bme280
import utime
import ntptime
import ujson
import time
from machine import Timer
from machine import Pin
import setup
from local_log import local_log

relay_pin = None
sensor = None
client = None
node_name = None

node_name = None
ssid = None
password = None
broker = None
period = None
sda_pin = None
scl_pin = None
log = None

def sensor_init():
    global sensor
    
    print("Initializing sensor.")

    pinSDA = machine.Pin(sda_pin)
    pinSCL = machine.Pin(scl_pin)

    i2c = machine.I2C(scl=pinSCL, sda=pinSDA)

    sensor = bme280.BME280(i2c=i2c)
    
def mqtt_init():
    global client
    print("Initializing MQTT client.")
    print("node name:", node_name)
    client = MQTTClient(node_name, broker)
    client.set_callback(mqtt_msg)

    client.connect()

def mqtt_msg(topic, msg):
    print("topic:", topic)
    print("message:", msg.decode("utf-8"))
    
    if topic.decode("utf-8") == (node_name + "/relay/set"):
        if msg.decode("utf-8") == 'OFF':
            print("LED OFF")
            client.publish(node_name + "/relay", "OFF")
            relay_pin.value(1)
        if msg.decode("utf-8") == 'ON':
            print("LED ON")
            client.publish(node_name + "/relay", "ON")
            relay_pin.value(0)
            
def sensor_read_handle(timer):
    sensor_read()
            
def sensor_read():
    global sensor
    global client
    
    #sensor.measure()
    temp,press,hum = sensor.read_compensated_data()

    # C
    temp = temp / 100
    # hPa
    press = press / 256
    press = press / 100
    # %
    hum = hum / 1024
    
    time = utime.localtime()
    
    print("sensor read:", temp,press,hum)
    
    try:
        client.publish(node_name + "/status", "online")
        client.publish(node_name + "/sens", "{ \"temp\": " + str(temp) +", \"hum\": " + str(hum) +", \"press\": " + str(press) + "}")
    except Exception as e:
        log.log_write("fail while publishing:", str(e))
        machine.reset()
        
def main ():
    # initialize watchdog
    wdt = machine.WDT(timeout=10000)
    
    global node_name 
    global ssid 
    global password 
    global broker 
    global period 
    global sda_pin 
    global scl_pin
    
    # read this from file
    json = setup.read_config("config.json")
    node_name = json["name"]
    ssid = json["ssid"]
    password = json["pass"]
    broker = json["broker"]
    sda_pin = json["sda_pin"]
    scl_pin = json["scl_pin"]
    period = int(json["period"])
    sleep_time = int(json["sleep_time"])
    sleep_flag = bool(json["sleep_flag"])
    
    log = local_log(node_name+".log")

    print("starting the sensor")
    log.log_write("starting the sensor")
    
    # ESP8266 watchdog workaround. Reset the MOFO
    wdt.feed()
    
    # connect to network
    try:
        setup.network_connect(ssid, password)
    except Exception as e:
        log.log_write("Setting up network err:" + str(e))
    
    # ESP8266 watchdog workaround
    wdt.feed()
    
    # Initialize DHT sensor
    sensor_init()
        
    # Initialize MQTT client and subscribe to rx_topic
    mqtt_init()
    try:
        if sleep_flag != True:
            print("NO SLEEP")
            tim = Timer(4)
            tim.init(mode=Timer.PERIODIC, period=period*1000, callback=sensor_read_handle)
        else:
            # ESP8266 watchdog workaround
            wdt.feed()
            
            sensor_read()
            
            # wait for MQTT stack to send before sleep
            time.sleep(1.5)
            
            print("Reseting the watchdog and sleep for " + str(sleep_time) + "seconds")
            wdt.feed()
            
            # put the device to sleep
            machine.deepsleep(sleep_time*1000)
    except Exception as e:
        log.log_write("exception: " + str(e))
        machine.reset()

    # shouldn't get to here
    print("Main done")
    machine.reset()

if __name__ == '__main__':
    main()

