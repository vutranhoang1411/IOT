import serial.tools.list_ports
# def getPort():
#     ports = serial.tools.list_ports.comports()
#     N = len(ports)
#     commPort = "None"
#     for i in range(0, N):
#         port = ports[i]
#         strPort = str(port)
#         if "USB Serial Device" in strPort:
#             splitPort = strPort.split(" ")
#             commPort = (splitPort[0])
#     return commPort

# def printPort():
#     ports = serial.tools.list_ports.comports()
#     N = len(ports)
#     commPort = "None"
#     for i in range(0, N):
#         port = ports[i]
#         strPort = str(port)
#         print(strPort)
wanted_id=0
ser = serial.Serial(port="/dev/pts/3", baudrate=115200)
mess = ""

def processData(client,data):
    #decode the data
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    # split[0]: data node id
    # split[1]: topic identifier
    # split[2]: payload
    received_id=int(splitData[0])
    global wanted_id
    if received_id==wanted_id:
        wanted_id=1-wanted_id
        publishData(client,splitData[1],splitData[2])
    sendSerial(f'!ACK:{wanted_id}')
    #publish to topics

        
def publishData(client,dev_id:str,data:str):
    if dev_id == "1":
        client.publish("cambien1",data)
    elif dev_id=="2":
        client.publish("cambien2",data)

    
def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client,mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]



def sendSerial(data):
    ser.write(str(data).encode("utf-8"))

serial_connect=False


# if __name__=="__main__":
#     while True:
#         readSerial()