"""
    If is needed to send data beetwen arduino and python, pyserial library es needed
    Install:
        python -m pip install pyserial

    When we get data from arduino we receive a class bytes, for example:
    If we send from arduino 
        Serial.println("Hello World!");
    
    In python using arduinoPort.readline() we'll receive a class bytes of len 14,
        b'Hello World!\r\n'
    
    We are not able to work with it as a string, that's why is needeed to convert it to UTF-8 encoding https://en.wikipedia.org/wiki/UTF-8
    python is able to do it with:
        data = str(arduinoPort.readline(),'utf-8')

    The message that we send ends with \n\r this is used to detect the end off line, but is not usefull for us, we can remove it doing [:-2]
        data = data[:-2]
    
    Now the message contains only the data that is usefull for us
"""   
import  serial #Module to use serial communication
import      re #Module to use regular expressions in Python
import logging #Module to log and prin messages with diferent  level
import     sys #Module with specific information system

print("{} Runnig serial example script {}".format("-"*10,"-"*10))
print("Send Identifier 9 to close script\n")

######################################################################
#                 ----- SETTING SERIAL PORT -----                    #
#    port: Specify the serial port where the arduino is connected    #
#       Windows         COMX                                         #
#       Linux      \dev\ttyX                                         #
#    baudRate: Specify the baudRate for serial port, the commontly   #
#               baudRate used is 1152001                             #
######################################################################
port='COM2'
baudRate=115200
arduinoPort = serial.Serial(port,baudRate)

class serialMessage:
    def __init__(self,identifier = -1, numbers = [0]):
        self.identifier = identifier
        self.numbers    = numbers
    def show(self):
        logging.debug("Identifier = {}\nNumbers: {}\n".format(self.identifier,self.numbers))

class serialFunction:
    def __init__(self,serialData,callBack):
        self.serialData = serialData
        self.callBack   = callBack 

def readSerialData(port):
    """
        Function: readSerialData
        Input:
            port = Serial PORT object
        Output:

    """
    ###############################################################################################################
    #                            ----- REGULAR EXPRESSION TO CHECK SERIAL INPUT -----                             #
    #                                                                                                             #
    #  https://platzi.com/tutoriales/1104-python-2017/1671-entendiendo-las-expresiones-regulares-con-python/      #
    #  When we receive a serial input is needed to verify if the entered                                          #
    #   expression is valid, for example:                                                                         #
    #       2_1,6,-32,4                                                                                           #
    #   The identifier number is 2 and 4 digits where entered with values                                         #
    #     value 1 =   1                                                                                           #
    #     value 2 =   6                                                                                           #                                                   
    #     value 3 = -32                                                                                           #
    #     value 4 =   4                                                                                           #
    #                                                                                                             #
    ###############################################################################################################

    serialPattern =  re.compile(r'[0-9]+_[-]?[0-9]+([,][-]?[0-9]+)*$')
    serialInput= str(port.readline(),'utf-8')[:-2]
    
    message = serialMessage()
    if serialPattern.match(serialInput):
        message.identifier = int(serialInput.split("_")[0])
        message.numbers    = list(map(int,serialInput.split("_")[1].split(",")))
        message.show()
    else:       
        logging.debug("The serial expression {} doesn't match".format(serialInput))
    
    return message

def sendSerialData(port,serialMessage):
    """
        sendSerialData is a function that takes a serialMessage,
        and send it by serial port
    """
    strMessage = str(serialMessage.identifier)+"_"

    loop=1
    for i in serialMessage.numbers:
        if loop == len(serialMessage.numbers):
            strMessage+=str(i)+"\n"
        else:
            strMessage+=str(i)+","
    port.write(strMessage.encode('ascii'))

running = True
while running:
    print("  p to get ADC pot value")
    print("  l to send LED value")
    option = input()

    if option == "p":
        message = serialMessage(2)
        sendSerialData(arduinoPort,message) 
        message = readSerialData(arduinoPort)
        print("Pot: {}".format(message.numbers[0]))
    elif option == "l":
        status = int(input("  1 ON\n  0 OFF\n"))
        print("Answer {}".format(status))
        if status == 0 or status == 1:
            message = serialMessage(4,[status])
            sendSerialData(arduinoPort,message)
        else:   
            print("Only 0 or 1 value accepted")   
       
    else:
        print("Exitin demo")
        running = False
      
print("Exiting APP ...")
arduinoPort.close()