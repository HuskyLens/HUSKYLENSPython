### HuskyLens Python Library 
### Author: Robert Prast (robert@dfrobot.com)
### 03/04/2020
### Dependenices :
###         pyserial 
###         smbus 
### How to use :
###         1) First import the library into your project and connect your HuskyLens
###         2) Init huskylens
###             A) Serial
###                huskyLens = HuskyLensLibrary("SERIAL","COM_PORT", speed) *speed is integer 
###             B) I2CD
###                huskyLens = HuskyLensLibrary("I2C","", address=0xADDR) *address is hex integer
###         4) Call your huskylens functions on the huskyLens object!
###
###
### Functions :
###        command_request()
###             => Return all data 
###
###        command_request_blocks()
###             => Return all blocks on the screen
###
###        command_request_arrows()
###             => Return all arrows on the screen
###
###        command_request_learned()
###             => Return all learned objects on screen
###
###        command_request_blocks_learned()
###             => Return all learned blocks on screen
###
###        command_request_arrows_learned() 
###             => Return all learned arrows on screen 
###
###        command_request_by_id(idVal)
###             *idVal is an integer
###             => Return the object with id of idVal
###
###        command_request_blocks_by_id(idVal) *idVal is an integer
###             *idVal is an integer
###             => Return the block with id of idVal
###        command_request_arrows_by_id(idVal) *idVal is an integer
###             *idVal is an integer
###             => Return the arrow with id of idVal
###
###
### Example code
'''
huskyLens = HuskyLensLibrary("I2C","",address=0x32)
huskyLens.command_request_algorthim("ALGORITHM_FACE_RECOGNITION")
while(true):
    data=huskyLens.command_request_blocks()
    x=0
    for i in data:
        x=x+1
        print("Face {} data: {}".format(x,i)
'''



import time
import serial
import smbus

commandHeaderAndAddress = "55AA11"
algorthimsByteID = {
    "ALGORITHM_OBJECT_TRACKING": "0100",
    "ALGORITHM_FACE_RECOGNITION": "0000",
    "ALGORITHM_OBJECT_RECOGNITION": "0200",
    "ALGORITHM_LINE_TRACKING": "0300",
    "ALGORITHM_COLOR_RECOGNITION": "0400",
    "ALGORITHM_TAG_RECOGNITION": "0500",
    "ALGORITHM_OBJECT_CLASSIFICATION": "0600"
}


class HuskyLensLibrary:
    def __init__(self, proto, comPort, speed=9600, channel=1, address=0x32):
        self.proto=proto
        self.address=address
        if(proto=="SERIAL"):
            self.huskylensSer = serial.Serial(
                port=comPort,
                baudrate=speed
            )
        elif (proto=="I2C"):
            self.huskylensSer= smbus.SMBus(channel)
        self.lastCmdSent = ""
        
    def writeToHuskyLens(self, cmd):
        self.lastCmdSent = cmd
        if(self.proto=="SERIAL"):
            self.huskylensSer.write(cmd)
        else:
            self.huskylensSer.write_i2c_block_data(self.address,12, list(cmd))


    def calculateChecksum(self, hexStr):
        total = 0
        for i in range(0, len(hexStr), 2):
            total += int(hexStr[i:i+2], 16)
        hexStr = hex(total)[-2:]
        return hexStr

    def cmdToBytes(self, cmd):
        return bytes.fromhex(cmd)

    def splitCommandToParts(self, str):
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
        if(self.proto=="SERIAL"):
                    byteString = self.huskylensSer.read(5)
                    byteString += self.huskylensSer.read(int(byteString[3]))
                    byteString += self.huskylensSer.read(1)
        else:
                    byteString=b''
                    for i in range(5):
                        byteString+=bytes([(self.huskylensSer.read_byte(self.address))])
                    for i in range(int(byteString[3])+1):
                        byteString+=bytes([(self.huskylensSer.read_byte(self.address))])
        
        commandSplit = self.splitCommandToParts(byteString.hex())
        return commandSplit[4]

    def processReturnData(self):
        inProduction = True
        if(inProduction):
            try:
                if(self.proto=="SERIAL"):
                    byteString = self.huskylensSer.read(5)
                    byteString += self.huskylensSer.read(int(byteString[3]))
                    byteString += self.huskylensSer.read(1)
                else:
                    byteString=b''
                    for i in range(5):
                        byteString+=bytes([(self.huskylensSer.read_byte(self.address))])
                    for i in range(int(byteString[3])+1):
                        byteString+=bytes([(self.huskylensSer.read_byte(self.address))])                    
                commandSplit = self.splitCommandToParts(byteString.hex())
                if(commandSplit[3] == "2e"):
                    return "Knock Recieved"
                else:
                    returnData = []
                    numberOfBlocksOrArrow = int(
                        commandSplit[4][2:4]+commandSplit[4][0:2], 16)
                    numberOfIDLearned = int(
                        commandSplit[4][6:8]+commandSplit[4][4:6], 16)
                    frameNumber = int(
                        commandSplit[4][10:12]+commandSplit[4][8:10], 16)
                    for i in range(numberOfBlocksOrArrow):
                        returnData.append(self.getBlockOrArrowCommand())
                    finalData=[]
                    tmp=[]
                    for i in returnData:
                        tmp=[]
                        for q in range(0,len(i),4):
                            low=int(i[q:q+2], 16)
                            high=int(i[q+2:q+4], 16)
                            #print(f"here are got low byte of {low} and high byte of {high}")
                            if(high>0):
                                val=low+255+high
                            else:
                                val=low
                            tmp.append(val)
                        finalData.append(tmp)
                        tmp=[]
                    return finalData
            except:
                 print("Read error")
                 return []
                
    def command_request_knock(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002c3c")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def command_request(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def command_request_blocks(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002131")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def command_request_arrows(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002232")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def command_request_learned(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002333")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def command_request_blocks_learned(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002434")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def command_request_arrows_learned(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002535")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def command_request_by_id(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0226"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def command_request_blocks_by_id(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0227"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def command_request_arrows_by_id(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0228"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def command_request_algorthim(self, alg):
        if alg in algorthimsByteID:
            cmd = commandHeaderAndAddress+"022d"+algorthimsByteID[alg]
            cmd += self.calculateChecksum(cmd)
            cmd = self.cmdToBytes(cmd)
            self.writeToHuskyLens(cmd)
            return self.processReturnData()
        else:
            print("INCORRECT ALGORITHIM NAME")