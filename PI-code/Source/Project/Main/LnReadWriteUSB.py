#!/usr/bin/python3
import sys
import serial
import time

import binascii

###############################################################
# Definizione delle porte
###############################################################
STX = b'\x02'
ETX = b'\x03'

def openRs232Port(portNO, baudRate=9600):
    devPort = '/dev/ttyUSB{0}'.format(portNO)
    print('Monitoring port: {0}'.format(devPort))

    try:
        port = serial.Serial(port=devPort,
                baudrate=baudRate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout = 6
            )
            # rtscts=1,
    except (Exception) as why:
        print()
        print ('    ERROR: ', str(why))
        print()
        sys.exit()

    return port

#######################################################################
# Lettura di una riga con il presupposto che '\n' indica fine riga
#######################################################################
def readData(port, hex=False, eod=b'\x0a'):
    retVal = bytearray()
    while True:
        ch = port.read(1)
        if ch:
            print ("{0} - {2:<10} {1}".format(type(ch), ch, ord(ch)))
            chHex = binascii.hexlify(ch)
            chInt = int(chHex, 16)
            if hex:
                print ("{0:02x} ".format(chInt), end='')
            else:
                print ("{0}".format(chr(chInt)), end='')
            retVal.append(ord(ch))
            if ch == eod:
                print ('FOUND')
                return retVal



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
    index = 0
    while True:
        index += 1
        # line = '[{0}:04] - {1}'.format(index, data)
        line = '[{0}:{1:04}] - {2}'.format(port.port, index, data)
        # print ("{0} - Sending:  {1}".format(port.port, data[:-1]))
        print ("Sending string:  {0}".format(line[:-1]))
        port.write(line.encode('utf-8'))
        time.sleep(5)





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


#######################################################################
# Lettura di dati fino ad eod
#######################################################################
codeType = 'utf8'

def LnRs485_Monitor(port, eod=ETX):
    while True:
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
        # time.sleep(1)






if __name__ == '__main__':
    Syntax = ("""
        Immettere:
        xxx.port.EOD   : action.usbPortNO.EoD [EOD=endOfData, default=10='\n']

        rline.0.10   : read line dalla ttyUSB0 (loop)
        wline.0.10   : write line dalla ttyUSB0 (loop every 5 sec)
        rdata.0.3    : read data dalla ttyUSB0 in formato Hex (loop)
        rhex.0.3     : read data dalla ttyUSB0 in formato Hex (loop)
        r485.0.3     : lread un dato rs485 dalla ttyUSB0
    """)

    if len(sys.argv) > 1:
        token = sys.argv[1].split('.')

        if len(token) == 2:
            what, portNO = sys.argv[1].split('.')
            EOD = b'\n'

        elif len(token) == 3:
            what, portNO, EOD = sys.argv[1].split('.')
            iEOD = int(EOD)
            EOD = bytes([iEOD])

        else:
            print (Sintax)


        print('     .....action:', what)
        print('     .....portNO:', portNO)
        print('     .....EOD:   ', EOD)


        if what in ['test']:  # t0, t1, t2, .. test - open/close the port
            port = openRs232Port(portNO, 9600)
            print('closing port: {0}'.format(devPort))
            port.close()

        elif what in ['r485']:
            port = openRs232Port(portNO, baudRate=9600)
            LnRs485_Monitor(port, eod=EOD)

        elif what in ['rline']:
            port = openRs232Port(portNO, baudRate=9600)
            readLine(port, eol=EOD)

        elif what in ['wline']:
            port = openRs232Port(portNO, baudRate=9600)
            writeLine(port, data='Invio dati....')

        elif what in ['rdata']:
            port = openRs232Port(portNO, baudRate=9600)
            while True:
                retData = readData(port, hex=False, eod=EOD)
                print ('full data:       {0}'.format(' '.join('{:02x}'.format(x) for x in retData)))
                sys.exit()

        elif what in ['rhex']:
            port = openRs232Port(portNO, baudRate=9600)
            # EOD = b'\n'
            # EOD = ETX
            while True:
                retData = readData(port, hex=True, eod=EOD)
                print ('full data:       {0}'.format(' '.join('{:02x}'.format(x) for x in retData)))
                sys.exit()


        else:
            print (Syntax)

    else:
        print (Syntax)


    sys.exit()

