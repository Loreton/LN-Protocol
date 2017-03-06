#!/usr/bin/python3
import sys
import serial
import time


###############################################################
# Definizione delle porte
###############################################################

def openRs232Port(portNO, baudRate=9600):
    devPort = '/dev/ttyUSB{0}'.format(portNO)
    print('Monitoring port: {0}'.format(devPort))

    port = serial.Serial(port=devPort,
            baudrate=baudRate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout = 6
        )
    return port

            # rtscts=1,

#######################################################################
# Lettura di una riga con il presupposto che '\n' indica fine riga
#######################################################################
def readData(port, eod=b'\n'):
    retVal = bytearray()
    while True:
        ch = port.read(1)
        if ch:
            print ("{0} - {1}".format(type(ch), ch))
            retVal.append(ord(ch))
            # if ch == b'\x03':
            if ch == eod:
                print ('TROVATO')
                return retVal



#######################################################################
# Lettura di dati fino ad eod
#######################################################################
codeType = 'utf8'
STX = b'\x02'
ETX = b'\x03'
def LnRs485_Monitor(port, eod=b'\n'):
    while True:
        print ('sono nel loop')
        retData = readData(port, eod)
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




#######################################################################
# Lettura di una riga con il presupposto che '\n' indica fine riga
#######################################################################
def readLine(port, eol='\n', trimNewLine=True):
    while True:
        line = port.readline()
        if line:
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            byte0 = line[0]
            # if byte0 == address:
            if trimNewLine: line=line.strip(eol)
            print ("{0} - {1}".format(port.port, line))
            # print ()
            # return line


#######################################################################
# Scrittura  di una riga con il presupposto che '\n' indica fine riga
#######################################################################
def writeLine(port, data):
    if data[-1] != '\n': data = data + '\n'
    print ("{0} - Sending:  {1}".format(port.port, data[:-1]))
    port.write(data.encode('utf-8'))





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
        portNO = param[-1]

        if param.startswith('test'):  # t0, t1, t2, .. test - open/close the port
            port = openRs232Port(portNO, 9600)
            print('closing port: {0}'.format(devPort))
            port.close()



        elif param.startswith('mon'):  # m0, m1, m2, .. monitor
            port = openRs232Port(portNO, baudRate=9600)
            LnRs485_Monitor(port, eod=ETX)

        elif param.startswith('line'):  # r0, r1, r2, .. ReadData fino alla ricezione del EoD - EndOfData
            port = openRs232Port(portNO, baudRate=9600)
            readLine(port, eol='\n')


    sys.exit()

