import sys
from Adafruit_IO import MQTTClient
from time import sleep
from hardware_connector import *
import threading
import detect_image
#######set up adafruit server
AIO_FEED_IDs = ["cambien1","cambien2","cambien3","nutnhan1"] #can get from env file
AIO_USERNAME = "vutranhoang1411"
AIO_KEY = "aio_JyWz99z2Ln5c80KUXCVuqIBjRhnq"

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

    if feed_id=="nutnhan1":
        if payload=="0":
            sendSerial("!BOFF#")
        elif payload=="1":
            sendSerial("!BON#")

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
