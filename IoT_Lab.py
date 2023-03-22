import sys
from Adafruit_IO import MQTTClient
from time import sleep
from hardware_connector import *
# from random import randint
# # from detect_image import *

# AIO_PATH="vutranhoang1411/feeds/"
AIO_FEED_IDs = ["cambien1","cambien2"] #can get from env file
AIO_USERNAME = "vutranhoang1411"
AIO_KEY = "aio_QWTb30HEwgJ0zcvt0O3odvAVMw6g"


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
    #do somethign with the dât
    print("Nhan du lieu: " + payload + " from feed: "+feed_id)
def on_publish(client,mid):
    print("On publish event with mid"+str(mid))
client.on_connect = on_connect
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.on_publish=on_publish
client.connect()
client.loop_background()

while True:
    readSerial(client)

    