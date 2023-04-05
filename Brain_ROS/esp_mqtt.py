from secrets import *
from serial import *
import time
import mqtt_CBR
    
mqttBroker = '10.245.151.187'
topicSub = 'dog/camera'
topicPub = 'dog/camera'
clientID = 'ESP'

def whenCalled(topic, msg):
    time.sleep(0.5)

mqtt_CBR.connect_wifi(Tufts_Wireless)
client = mqtt_CBR.mqtt_client(clientID, mqttBroker, whenCalled)
client.subscribe(topicSub)

