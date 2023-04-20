import sys
from Adafruit_IO import MQTTClient
from time import sleep
from hardware_connector import *
import threading
import detect_image
#######set up adafruit server
AIO_FEED_IDs = ["iot-hk222.pump"] #can get from env file
# AIO_USERNAME = "vutranhoang1411"
# AIO_KEY = "aio_fVka33U5AthCsw0KlHzeRqQO0uAE"
AIO_USERNAME = "vynguyen08122002"
AIO_KEY = "aio_jTpa00iRWo7ACInoo8sMTJ1I7Pr8"


client = MQTTClient(AIO_USERNAME,AIO_KEY)

def on_connect(client):
    print("Ket noi thanh cong!")
    for feed in AIO_FEED_IDs:
        client.subscribe(feed)
    
def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):

    if feed_id=="iot-hk222.pump":
        if payload=="0":
            sendSerial("!BOFF#")
        elif payload=="1":
            sendSerial("!BON#")
    else:
        print(payload)

client.on_connect = on_connect
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
sleep(5)

########## read serial
def ReadSerial():
    while True:
        readSerial(client)

threading.Thread(target=ReadSerial).start()

##### detect img
AI_Cam=detect_image.AICam("./employee",client)
AI_Cam.StartRecord()
