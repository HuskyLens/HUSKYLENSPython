# HuskyLens Python Library
# Author: Robert Prast (robert@dfrobot.com)
# 08/03/2020
# Dependenices :
#   pyserial
#   smbus
#   pypng
#
# How to use :
# 1) First import the library into your project and connect your HuskyLens
# 2) Init huskylens
#   A) Serial
#          huskyLens = HuskyLensLibrary("SERIAL","COM_PORT", speed) *speed is integer
#   B) I2C
#           huskyLens = HuskyLensLibrary("I2C","", address=0xADDR) *address is hex integer
# 3) Call your desired functions on the huskyLens object!
###
# Example code
'''
huskyLens = HuskyLensLibrary("I2C","",address=0x32)
huskyLens.algorthim("ALGORITHM_FACE_RECOGNITION")
while(true):
    data=huskyLens.blocks()
    x=0
    for i in data:
        x=x+1
        print("Face {} data: {}".format(x,i)
'''


import time
import serial
import png
import json


commandHeaderAndAddress = "55AA11"
algorthimsByteID = {
    "ALGORITHM_OBJECT_TRACKING": "0100",
    "ALGORITHM_FACE_RECOGNITION": "0000",
    "ALGORITHM_OBJECT_RECOGNITION": "0200",
    "ALGORITHM_LINE_TRACKING": "0300",
    "ALGORITHM_COLOR_RECOGNITION": "0400",
    "ALGORITHM_TAG_RECOGNITION": "0500",
    "ALGORITHM_OBJECT_CLASSIFICATION": "0600",
    "ALGORITHM_QR_CODE_RECOGNTITION" : "0700",
    "ALGORITHM_BARCODE_RECOGNTITION":"0800",
}

class Arrow:
    def __init__(self, xTail, yTail , xHead , yHead, ID):
        self.xTail=xTail
        self.yTail=yTail
        self.xHead=xHead
        self.yHead=yHead
        self.ID=ID
        self.learned= True if ID > 0 else False
        self.type="ARROW"


class Block:
    def __init__(self, x, y , width , height, ID):
        self.x = x
        self.y=y
        self.width=width
        self.height=height
        self.ID=ID
        self.learned= True if ID > 0 else False
        self.type="BLOCK"



class HuskyLensLibrary:
    def __init__(self, proto, comPort="", speed=3000000, channel=1, address=0x32):
        self.proto = proto
        self.address = address
        self.checkOnceAgain=True
        if(proto == "SERIAL"):
            self.huskylensSer =serial.Serial(
                baudrate=speed,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=.5
            )
            self.huskylensSer.dtr = False
            self.huskylensSer.rts = False
            time.sleep(.1)
            self.huskylensSer.port=comPort
            self.huskylensSer.open()
            time.sleep(2)
            self.knock()
            time.sleep(.5)
            self.knock()
            time.sleep(.5)
            self.knock()
            # self.huskylensSer.timeout=5
            self.huskylensSer.flushInput()
            self.huskylensSer.flushOutput()
            self.huskylensSer.flush()

        elif (proto == "I2C"):
            import smbus
            self.huskylensSer = smbus.SMBus(channel)
        self.lastCmdSent = ""

    def writeToHuskyLens(self, cmd):
        self.lastCmdSent = cmd
        if(self.proto == "SERIAL"):
            self.huskylensSer.flush()
            self.huskylensSer.flushInput()
            self.huskylensSer.write(cmd)
        else:
            self.huskylensSer.write_i2c_block_data(self.address, 12, list(cmd))

    def calculateChecksum(self, hexStr):
        total = 0
        for i in range(0, len(hexStr), 2):
            total += int(hexStr[i:i+2], 16)
        hexStr = hex(total)[-2:]
        return hexStr

    def cmdToBytes(self, cmd):
        return bytes.fromhex(cmd)

    def splitCommandToParts(self, str):
        # print(f"We got this str=> {str}")
        headers = str[0:4]
        address = str[4:6]
        data_length = int(str[6:8], 16)
        command = str[8:10]
        if(data_length > 0):
            data = str[10:10+data_length*2]
        else:
            data = []
        checkSum = str[2*(6+data_length-1):2*(6+data_length-1)+2]

        return [headers, address, data_length, command, data, checkSum]

    def getBlockOrArrowCommand(self):
        if(self.proto == "SERIAL"):
            byteString = self.huskylensSer.read(5)
            byteString += self.huskylensSer.read(int(byteString[3]))
            byteString += self.huskylensSer.read(1)
        else:
            byteString = b''
            for i in range(5):
                byteString += bytes([(self.huskylensSer.read_byte(self.address))])
            for i in range(int(byteString[3])+1):
                byteString += bytes([(self.huskylensSer.read_byte(self.address))])

        commandSplit = self.splitCommandToParts(byteString.hex())
        isBlock = True if commandSplit[3] == "2a" else False
        return (commandSplit[4],isBlock)

    def processReturnData(self, numIdLearnFlag=False, frameFlag=False):
        inProduction = True
        byteString=""
        if(inProduction):
            try:
                if(self.proto == "SERIAL"):
                    byteString = self.huskylensSer.read(5)
                    byteString += self.huskylensSer.read(int(byteString[3]))
                    byteString += self.huskylensSer.read(1)
                else:
                    byteString = b''
                    for i in range(5):
                        byteString += bytes([(self.huskylensSer.read_byte(self.address))])
                    for i in range(int(byteString[3])+1):
                        byteString += bytes([(self.huskylensSer.read_byte(self.address))])
                commandSplit = self.splitCommandToParts(byteString.hex())
                # print(commandSplit)
                if(commandSplit[3] == "2e"):
                    self.checkOnceAgain=True
                    return "Knock Recieved"
                else:
                    returnData = []
                    numberOfBlocksOrArrow = int(
                        commandSplit[4][2:4]+commandSplit[4][0:2], 16)
                    numberOfIDLearned = int(
                        commandSplit[4][6:8]+commandSplit[4][4:6], 16)
                    frameNumber = int(
                        commandSplit[4][10:12]+commandSplit[4][8:10], 16)
                    isBlock=True
                    for i in range(numberOfBlocksOrArrow):
                        tmpObj=self.getBlockOrArrowCommand()
                        isBlock=tmpObj[1]
                        returnData.append(tmpObj[0])

                    
                    # isBlock = True if commandSplit[3] == "2A"else False
                    
                    finalData = []
                    tmp = []
                    # print(returnData)
                    for i in returnData:
                        tmp = []
                        for q in range(0, len(i), 4):
                            low=int(i[q:q+2], 16)
                            high=int(i[q+2:q+4], 16)
                            if(high>0):
                                val=low+255+high
                            else:
                                val=low
                            tmp.append(val)
                        finalData.append(tmp)
                        tmp = []
                    self.checkOnceAgain=True
                    ret=self.convert_to_class_object(finalData,isBlock)
                    if(numIdLearnFlag):
                        ret.append(numberOfIDLearned)
                    if(frameFlag):
                        ret.append(frameNumber)
                    return ret
            except:
                if(self.checkOnceAgain):
                    self.huskylensSer.timeout=5
                    self.checkOnceAgain=False
                    self.huskylensSer.timeout=.5
                    return self.processReturnData()
                print("Read response error, please try again")
                self.huskylensSer.flushInput()
                self.huskylensSer.flushOutput()
                self.huskylensSer.flush()
                return []

    def convert_to_class_object(self,data,isBlock):
        tmp=[]
        for i in data:
            if(isBlock):
                obj = Block(i[0],i[1],i[2],i[3],i[4])
            else:
                obj = Arrow(i[0],i[1],i[2],i[3],i[4])
            tmp.append(obj)
        return tmp

    def knock(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002c3c")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def learn(self,x):
        data = "{:04x}".format(x)
        part1=data[2:]
        part2=data[0:2]
        #reverse to correct endiness
        data=part1+part2
        dataLen = "{:02x}".format(len(data)//2)
        cmd = commandHeaderAndAddress+dataLen+"36"+data
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def forget(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"003747")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def setCustomName(self,name,idV):
        nameDataSize = "{:02x}".format(len(name)+1)
        name = name.encode("utf-8").hex()+"00"
        localId = "{:02x}".format(idV)
        data = localId+nameDataSize+name
        dataLen = "{:02x}".format(len(data)//2)
        cmd = commandHeaderAndAddress+dataLen+"2f"+data
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def customText(self,nameV,xV,yV):
        name=nameV.encode("utf-8").hex()
        nameDataSize = "{:02x}".format(len(name)//2)
        if(xV>255):
            x="ff"+"{:02x}".format(xV%255)
        else:
            x="00"+"{:02x}".format(xV)
        y="{:02x}".format(yV)

        data = nameDataSize+x+y+name
        dataLen = "{:02x}".format(len(data)//2)

        cmd = commandHeaderAndAddress+dataLen+"34"+data
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def clearText(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"003545")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def requestAll(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def saveModelToSDCard(self,idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0232"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def loadModelFromSDCard(self,idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0233"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def savePictureToSDCard(self):
        self.huskylensSer.timeout=5
        cmd = self.cmdToBytes(commandHeaderAndAddress+"003040")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def saveScreenshotToSDCard(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"003949")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def blocks(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002131")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def arrows(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002232")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def learned(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002333")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def learnedBlocks(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002434")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def learnedArrows(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002535")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def getObjectByID(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0226"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def getBlocksByID(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0227"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def getArrowsByID(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0228"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def algorthim(self, alg):
        if alg in algorthimsByteID:
            cmd = commandHeaderAndAddress+"022d"+algorthimsByteID[alg]
            cmd += self.calculateChecksum(cmd)
            cmd = self.cmdToBytes(cmd)
            self.writeToHuskyLens(cmd)
            return self.processReturnData()
        else:
            print("INCORRECT ALGORITHIM NAME")

    def count(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return len(self.processReturnData())
    
    def learnedObjCount(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return self.processReturnData(numIdLearnFlag=True)[-1]
    
    def frameNumber(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return self.processReturnData(frameFlag=True)[-1]

