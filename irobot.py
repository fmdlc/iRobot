import paho.mqtt.client as mqtt
import argparse
import sys
import ssl

parser = argparse.ArgumentParser()
parser.add_argument("--username", help="iRobot username")
parser.add_argument("--password", help="iRobot password")
parser.add_argument("--ip", help="iRobot IP address")
parser.add_argument("--port", type=int, default=1883, help="iRobot Port (default: 1883)")
parser.add_argument("--emitInterval", type=int, default=800, help="Emit Interval (default: 800)")
args = parser.parse_args()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# posibleCap = ['pose', 'ota', 'multiPass', 'carpetBoost', 'pp', 'binFullDetect', 'langOta', 'maps', 'edge', 'eco', 'svcConf']

options = {"port": 8883,
           "clientId": args.username,
           "rejectUnauthorized": "false",
           "protocolId": "MQTT",
           "protocolVersion": 4,
           "ciphers": 'AES128-SHA256',
           "clean": "false",
           "username": args.username,
           "password":args.password
           }

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(args.ip, options['port'])
    print("Connected to: {}".format(args.ip))
except(ConnectionRefusedError):
    print("Unable to connect: Connection refused")
    sys.exit(1)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client.disconnect()
print("Client disconnected")
