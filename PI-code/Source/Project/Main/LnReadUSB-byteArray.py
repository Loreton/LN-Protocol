#!/usr/bin/python3
import sys
import serial
import time


###############################################################
# Definizione delle porte
###############################################################

def openRs232Port(devPort='/dev/ttyUSB0', baudRate=9600):
    port = serial.Serial(port=devPort,
            baudrate=baudRate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout = 6
        )
    return port

# port0 = serial.Serial(port='/dev/ttyUSB0',
#         baudrate=115200,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS,
#         timeout = 6
#     )

# port1 = serial.Serial(port='/dev/ttyUSB1',
#         baudrate=115200,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS,
#         timeout = 6
#     )

# port2 = serial.Serial(port='/dev/ttyUSB2',
#         baudrate=115200,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS,
#         timeout = 6
#     )

#######################################################################
# Lettura di una riga con il presupposto che '\n' indica fine riga
#######################################################################
def readLine(port, address, trimNewLine=True):
    line = port.readline()
    if line:
        if isinstance(line, bytes):
            line = line.decode('utf-8')
        byte0 = line[0]
        if byte0 == address:
            print ("{0} - Received: {1}".format(port.port, line))
            if trimNewLine: line=line.strip('\n')
            return line


#######################################################################
# Scrittura  di una riga con il presupposto che '\n' indica fine riga
#######################################################################
def writeLine(port, data):
    if data[-1] != '\n': data = data + '\n'
    print ("{0} - Sending:  {1}".format(port.port, data[:-1]))
    port.write(data.encode('utf-8'))



#######################################################################
# Lettura di una riga con il presupposto che '\n' indica fine riga
#######################################################################
def readData(port):
    retVal = bytearray()
    while True:
        ch = port.read(1)
        if ch:
            print ("{0} - {1}".format(type(ch), ch))
            retVal.append(ord(ch))
            if ch == b'\x03':
                print ('TROVATO')
                return retVal


codeType = 'utf8'
STX = '\x02'
ETX = '\x03'
#######################################################################
# Scrittura di chr sulla seriale
#######################################################################
def writeData(port, Address, data):
    xmitData = bytearray()
    xmitData.extend(STX.encode(codeType))
    xmitData.append(Address)
    xmitData.append(len(data))
    if isinstance(data, str):
        data = data.encode(codeType)
    xmitData.extend(data)
    xmitData.extend(ETX.encode(codeType))
    print ("{0} - Sending data:  {1}".format(port.port, xmitData))
    port.write(xmitData)



def Monitor(portNO):
    devPort = '/dev/ttyUSB{0}'.format(portNO)
    print('Monitoring port: {0}'.format(devPort))
    port = openRs232Port(devPort, 9600)

    while True:
        print ('sono nel loop')
        retData = readData(port)
        stx     = retData[0]
        Address = retData[1]
        dataLen = retData[2]
        data    = retData[3:]
        print ('stx:        {0:02x}'.format(stx))
        print ('Address:    {0:02x}'.format(Address))
        print ('dataLen:    {0:02x}'.format(dataLen))
        # print ('data:       {0}'.format(data))
        print ('full data:       {0}'.format(' '.join('{:02x}'.format(x) for x in retData)))
        print ()
        # sys.exit()
        time.sleep(1)


def startSlave(Address):
    if Address == 0:
        port = openRs232Port('/dev/ttyUSB0', 9600)
    elif Address == 1:
        port = openRs232Port('/dev/ttyUSB1', 9600)
    else:
        return

    while True:
        print ('sono nel loop')
        retData = readData(port, Address=Address)
        stx     = retData[0]
        Address = retData[1]
        dataLen = retData[3]
        data    = retData[4:-1]
        print (data.encode(codeType))
        # sys.exit()
        time.sleep(1)





def Test(portNO):
    devPort = '/dev/ttyUSB{0}'.format(portNO)
    print('opening port: {0}'.format(devPort))
    port = openRs232Port(devPort, 9600)
    print('closing port: {0}'.format(devPort))
    port.close()



def Master():
    myPort = port0
    counter = 0
    while True:
        counter += 1
        if counter%2:
            destAddress = 1
        else:
            destAddress = 2
        data = "Sending counter: {1}".format(destAddress, counter)
        # writeLine(myPort, data)
        writeData(myPort, 1, data)
        time.sleep(5)







if __name__ == '__main__':
    if len(sys.argv) > 1:
        param = sys.argv[1]
        if param.startswith('t'):  # t0, t1, t2, .. test - open/close the port
            Test(param[1])
        elif param.startswith('m'):  # m0, m1, m2, .. monitor - open/close the port
            Monitor(param[1])


    sys.exit()

