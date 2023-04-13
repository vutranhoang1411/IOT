from time import sleep
import serial.tools.list_ports

ser = serial.Serial(port="/dev/pts/4", baudrate=115200)
mess = ""
val={"temp":"0","humi":"0","lux":"0"}
def preProcessData(data:str)->str:
    start=-1
    for c in range(len(data)):
        if data[c]=='!':
            start=c
    data=data[start:]
    data = data.replace("!", "")
    data = data.replace("#", "")
    return data
def processData(client,data:str):
    #decode the data
    data=preProcessData(data)
    # !temp:<number>,humi:<number>,lux:<number>#
    deviceDatas=data.split(",")
    
    if len(deviceDatas)<3:
        return
    
    newPacket=False
    for devData in deviceDatas:
        devName=devData.split(":")[0]
        devPayload=devData.split(":")[1]
        if devPayload!=val[devName]:
            newPacket=True
            val[devName]=devPayload
            publishData(client,devName,devPayload)
    sendSerial("!ACK#")
    if newPacket:
        sleep(5)
        
    
    #publish to topics

        
def publishData(client,devName:str,devPayload:str):
    if devName == "temp":
        client.publish("cambien1",devPayload)
    elif devName=="humi":
        client.publish("cambien2",devPayload)
    elif devName=="lux":
        client.publish("cambien3",devPayload)

    
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



# if __name__=="__main__":
#     while True:
#         readSerial()