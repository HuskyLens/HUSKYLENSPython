
# HuskyLens Raspberry Pi Tutorial


# I. I2C Wiring Guide 

The primary protocol for communication between the HuskyLens and a Raspberry PI is I2C. This requires you to use the 4PIN connector to wrire ground, power, SDA, and SCL. To read more about how I2C works, please check out the following link:  https://en.wikipedia.org/wiki/I%C2%B2C

#### Pin Outline

![CI2C Wiring Guide ](http://www.raspberrypirobotics.com/wp-content/uploads/2018/01/Raspberry-pi-I2C-pins.png)

> ### I2C Wiring
>
> The 4 pin connector located on the bottom left has the following connections T, R , -, + (from left to right). Simply connect - and + to ground and 3.3-5.0V power respectively. Your T and R pins will connect to SDA and SCL pins on your Raspbery Pi. The blue R wire will connect to the SCL1 pin and the green T wire will connec to the SDA1, please refer the above picture where the SDA1 and SCL1 pins are outlined in red. 

##### Important Note

You must choose the protocol type and speed on the HuskyLens. Therefore, use the function to navigate to General Settings and then click Protocol. You can now use the function button again to choose I2C .

![Wiring](https://i.ibb.co/YydCcV4/101583380990-pic.jpg)

# II. Setting up the Raspberry PI 

On your Raspberry PI you must enable I2C in settings before being able to use it. Therefore open a terminal on your Raspberry PI and run the following commands

> 1) Run ```sudo raspi-config```
> 2) Use the down arrow to select 5 Interfacing Options
> 3) Arrow down to P5 I2C.
> 4) Select yes when it asks you to enable I2C
> 5) Also select yes if it asks about automatically loading the kernel module.
> 6) Use the right arrow to select the <Finish> button.
> 7) Select yes when it asks to reboot.
> 8) After reboot , run ```sudo apt-get install -y i2c-tools```
> 9) Run ```sudo apt-get install python-smbus```
> 10) Run ```sudo pip3 install pyserial```

# III. Coding Guide 

1) Download the Python Library here "INSERT_GITHUB_LINK_HERE"
2) Run ```sudo i2cdetect -y 1``` 
    > Please remember the address that pops up here, in my case it is 32. This is the I2C address for the HuskyLens
    If the above command returns an error please change to : ```sudo i2cdetct -y 0```

>```sh
>pi@raspberry: sudo i2cdetect -y 1
>0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
>00:          -- -- -- -- -- -- -- -- -- -- -- -- --
>10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
>20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
>30: -- -- 32 -- -- -- -- -- -- -- -- -- -- -- -- --
>40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
>50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
>60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
>70: -- -- -- -- -- -- -- --
>```
>
> 3) Place the huskylensPythonLibrary.py in your projects folder
> 4) In your python file , example test.py, import the library using
>
>```python 
> from huskylensPythonLibrary import HuskyLensLibrary
>```

 ```
 5) Init the HuskyLens 
 ```python
 # replace the address value with your I2C address from before in 0x00 form
 my_Var= HuskyLensLibrary("I2C","",address=0x32)
 ```

6) Now begin calling functions !

```python
 my_Var= HuskyLensLibrary("I2C","",address=0x32)
 # Check if HuskyLens can recieve commands
 print(my_Var.command_request_knock())
 # Get all the current blocks on screen
 blocks=my_Var.command_request_blocks()
 # Print the data
 print(blocks)
```

# IV. HuskyLens Functions

``` text
command_request()
     => Return all data 
     
command_request_blocks()
     => Return all blocks on the screen

command_request_arrows()
     => Return all arrows on the screen

command_request_learned()
     => Return all learned objects on screen

command_request_blocks_learned()
     => Return all learned blocks on screen

command_request_arrows_learned() 
     => Return all learned arrows on screen 

command_request_by_id(idVal)
     *idVal is an integer
     => Return the object with id of idVal

command_request_blocks_by_id(idVal) *idVal is an integer
     *idVal is an integer
     => Return the block with id of idVal

command_request_arrows_by_id(idVal) *idVal is an integer
     *idVal is an integer
     => Return the arrow with id of idVal

command_request_algorthim(ALG_NAME)
    * ALG_NAME is a string whose value can be the following
        "ALGORITHM_OBJECT_TRACKING"
        "ALGORITHM_FACE_RECOGNITION"
        "ALGORITHM_OBJECT_RECOGNITION"
        "ALGORITHM_LINE_TRACKING"
        "ALGORITHM_COLOR_RECOGNITION"
        "ALGORITHM_TAG_RECOGNITION"
        "ALGORITHM_OBJECT_CLASSIFICATION"

command_request_knock()
    => Returns "Knock Recieved" on success
```

# V. Example code

test.py

```python
# Import the library
from huskylensPythonLibrary import HuskyLensLibrary
# Initlialize the HuskyLens
test = HuskyLensLibrary("I2C","",address=0x32)
print("First request a knock: {}".format(test.command_request_knock()))

# Change to facial recognition algorhtim
test.command_request_algorthim("ALGORITHM_FACE_RECOGNITION")

# Display a simple menu where you can call every function in a loop!
ex=1
print("""
        Menu options:
        1) command_request()
        2) command_request_blocks()
        3) command_request_arrows()
        4) command_request_learned()
        5) command_request_blocks_learned()
        6) command_request_arrows_learned()
        7) command_request_by_id() ***format 7 ID_VAL***
        8) command_request_blocks_by_id() ***format 8 ID_VAL***
        9) command_request_arrows_by_id() ***format 9 ID_VAL***
        10) Exit
        """)
while(ex==1):
    v=input("Enter cmd number:")
    numEnter=v
    if(numEnter=="10"):
        ex=0
    v=int(v[0])
    if(v==1):
        print(test.command_request())
    elif(v==2):
        print(test.command_request_blocks())
    elif(v==3):
        print(test.command_request_arrows())
    elif(v==4):
        print(test.command_request_learned())
    elif(v==5):
        print(test.command_request_blocks_learned())
    elif(v==6):
        print(test.command_request_arrows_learned())
    elif(v==7):
        print(test.command_request_by_id(int(numEnter[2:])))
    elif(v==8):
        print(test.command_request_blocks_by_id(int(numEnter[2:])))
    elif(v==9):
        print(test.command_request_arrows_by_id(int(numEnter[2:])))
```


