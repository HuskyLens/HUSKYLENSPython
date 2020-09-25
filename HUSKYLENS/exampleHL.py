import random
import time
import json
from huskylib import HuskyLensLibrary

hl = HuskyLensLibrary("SERIAL", "/dev/ttyUSB1", 3000000)
# hl = HuskyLensLibrary("I2C","", address=0x32)

algorthimsByteID = {
    "ALGORITHM_OBJECT_TRACKING": "0100",
    "ALGORITHM_FACE_RECOGNITION": "0000",
    "ALGORITHM_OBJECT_RECOGNITION": "0200",
    "ALGORITHM_LINE_TRACKING": "0300",
    "ALGORITHM_COLOR_RECOGNITION": "0400",
    "ALGORITHM_TAG_RECOGNITION": "0500",
    "ALGORITHM_OBJECT_CLASSIFICATION": "0600",
    "ALGORITHM_QR_CODE_RECOGNTITION": "0700",
    "ALGORITHM_BARCODE_RECOGNTITION": "0800",
}
commandList = ['knock()', 
               'setCustomName() #Random String & Cords', 
               'customText() #Random String & Cords', 
               'clearText()', 
               'requestAll()', 
               'saveModelToSDCard(1)', 
               'loadModelFromSDCard(1)', 
               'savePictureToSDCard()', 
               'count()',
               'learnedObjCount()',
               'saveScreenshotToSDCard()', 
               'blocks()', 
               'arrows()', 
               'learned()', 
               'learnedBlocks()', 
               'learnedArrows()', 
               'getObjectByID(1)', 
               'getBlocksByID(1)', 
               'getArrowsByID(1)', 
               'algorthim() #Random Choice', 
               'learn(1)', 
               'forget()', 
               'frameNumber()',
               ""
            ]


def printMenu():
    print("**********************************************************"*2)
    print("MENU OPTIONS:")
    for i in range(0, len(commandList)-1, 2):
        part1 = chr(i+97)+"). "+commandList[i].ljust(45, " ")
        print(part1+chr(i+1+97)+"). "+commandList[i+1]+"\t\t ")
    print("[*] TYPE \"MENU\" to show the command menu[*]")
    print("[*] TYPE \"QUIT\" to quit[*]")
    print("**********************************************************"*2)
    print("")

def printObjectNicely(obj):
    count=1
    if(type(obj)==list):
        for i in obj:
            print("\t "+ ("BLOCK_" if i.type=="BLOCK" else "ARROW_")+str(count)+" : "+ json.dumps(i.__dict__))
            count+=1
    else:
        print("\t "+ ("BLOCK_" if obj.type=="BLOCK" else "ARROW_")+str(count)+" : "+ json.dumps(obj.__dict__))


ex = 1
printMenu()
while(ex == 1):
    try:
        v = input("Enter cmd letter:")
        if(v == "QUIT"):
            ex = 0
            print("QUITING")
            break
        if(v == "MENU"):
            printMenu()
            continue
        print('[*] COMMAND -> '+commandList[ord(v)-97] + '[*]')
        print("[*] RESPONSE [*]")
        numEnter = v
        v = v[0].lower()
        if(v == 'a'):
            print("\t"+hl.knock())

        elif(v == 'b'):
            print("\t"+hl.setCustomName(
                "test_"+str(random.randint(1, 10)), random.randint(1, 3)))

        elif(v == 'c'):
            print("\t"+hl.customText(
                "hl", random.randint(5, 300), random.randint(5, 200)))

        elif(v == 'd'):
            print("\t"+hl.clearText())

        elif(v == 'e'):
            printObjectNicely(hl.requestAll())

        elif(v == 'f'):
            print("\t"+hl.saveModelToSDCard(99))

        elif(v == 'g'):
            print("\t"+hl.loadModelFromSDCard(99))

        elif(v == 'h'):
            print("\t"+hl.savePictureToSDCard())

        elif(v == 'i'):
            print("\t"+str(hl.count()))

        elif(v == 'j'):
            print("\t"+str(hl.learnedObjCount()))

        elif(v == 'k'):
            print("\t"+hl.saveScreenshotToSDCard())

        elif(v == 'l'):
            printObjectNicely(hl.blocks())

        elif(v == 'm'):
            printObjectNicely(hl.arrows())

        elif(v == 'n'):
            printObjectNicely(hl.learned())

        elif(v == 'o'):
            printObjectNicely(hl.learnedBlocks())

        elif(v == 'p'):
            printObjectNicely(hl.learnedArrows())

        elif(v == 'q'):
            printObjectNicely(hl.getObjectByID(1))

        elif(v == 'r'):
            printObjectNicely(hl.getBlocksByID(1))

        elif(v == 's'):
            printObjectNicely(hl.getArrowsByID(1))

        elif(v == 't'):
            algs = list(algorthimsByteID.keys())
            a = algs[random.randint(0, 6)]
            print("\t"+hl.algorthim(a))

        elif(v == 'u'):
            print("\t"+hl.learn(1))

        elif(v == 'v'):
            print("\t"+hl.forget())

        elif(v == 'w'):
            print("\t"+hl.frameNumber())

        print("")
    except KeyboardInterrupt:
        print("\nQUITING")
        quit()
    # except TypeError:
    #     print("Please enter only a single letter")
    except IndexError:
        print(f"Command {v} not found")
    except Exception as e:
        # General error -> just print it
        print(f"Error {e}")


