# MQTT Example.
# This example shows how to use the MQTT library to publish to a topic.
#
# 1) Copy the mqtt.py library to OpenMV storage.
# 2) Run this script on the OpenMV camera.
# 3) Install the mosquitto client on PC and run the following command:
#    mosquitto_sub -h test.mosquitto.org -t "openmv/test" -v
#
# NOTE: If the mosquitto broker is unreachable, try another broker (For example: broker.hivemq.com)
import time, network
from mqtt import MQTTClient

# !!!! consider formatting more like Chris' example importing wifi from secrets.py and other checks below
SSID='RoseiPhone' # Network SSID
KEY='robodogrose'  # Network key

# Init wlan module and connect to network
print("Trying to connect. Note this may take a while...")

wlan = network.WLAN(network.STA_IF) # configure network
#print("scan\n",wlan.scan())
wlan.deinit()
wlan.active(True)
print("status\n",wlan.status())
wlan.connect(SSID, KEY, timeout=30000) # connect to wifi network

# We should have a valid IP now via DHCP
print("WiFi Connected ", wlan.ifconfig()) # interesting don't put ip directly in?

# create instance of MQTTClient class
# client_id, server/brokerip, port, keepalive
# use "test.mosquitto.org" as server/broker if want (beware broker may restart in testing, but not worth programming to cope w this b/c will use ros anyways)
client = MQTTClient("rosedog", "test.mosquitto.org", port=1883, keepalive=60) # Chris suggested adding this (found out from Mohammed), hopefully this is the right spot, I'm looking at library file of mqtt.py
client.connect()

count = 1
while (True):
    try:
        client.check_msg()
        client.publish("openmv/robotdog", str(count))
        time.sleep_ms(1000)
    except OSError as e:
        print(e)
        client.connect()
    except KeyboardInterrupt as e:
        client.disconnect()
        print('done')
        break
    count += 1
