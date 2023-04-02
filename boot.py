# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
import setup
import sys
import time

print("Booting up ...")
time.sleep(5)
print("Setting up the watchdog timer")
wdt = machine.WDT(timeout=30000)
sys.path.append('/libs')
sys.path.append('/')

conf = setup.read_config("config.json")
print("Config JSON:",conf)
setup.network_connect(conf["ssid"], conf["pass"])

# TODO: implement debug flag
#webrepl.start()

gc.collect()

wdt.feed()

# import app
import app_bme
app_bme.main()