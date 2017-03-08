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
# Ritorna una bytearray di integer
#######################################################################
def readDataInt(port, fPRINT=False, eod=b'\x0a'):
    retVal = bytearray()
    while True:
        ch = port.read(1)       # ch e' un bytes
        if ch == b'': continue

        chHex = binascii.hexlify(ch)
        chInt = int(chHex, 16)
        if fPRINT: print (  """     Received: {chTYPE} - char: {ordCH:<4} int:{intCH:5} hex:{hexCH:02x}
                            """.format(chTYPE=type(ch), ordCH=chr(ord(ch)),  intCH=chInt, hexCH=chInt)
                    )
        retVal.append(chInt)



        if ch == eod:
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

def LnRs485_Monitor(port, eod=ETX, fDEBUG=False):
    while True:
            # leggiamo i dati dalla seriale
        retData = readDataInt(port, fPRINT=False, eod=eod)
        print ('full data:       {0}'.format(' '.join('{:02x}'.format(x) for x in retData)))




            # Prendiamo i dati fissi
        startOfText     = retData[0]
        endOfText       = retData[-1]
        payLoadNibbled  = retData[1:-1] # skip STX and ETX - include nibbled_data+nibbled_CRC

            # ---------------------------------------------
            # - ricostruzione dei bytes originari
            # - byte = byte1_HighNibble*16 + byte2_HighNibble
            # ---------------------------------------------
            # il trick che segue ci permette di prelevare due bytes alla volta
        payLoad_crc = bytearray()
        xy = iter(payLoadNibbled)
        for ch1, ch2 in zip(xy, xy):
            realByte = combineComplementedByte(ch1, ch2, fDEBUG=False)
            if not realByte:
                return bytearray()
            else:
                payLoad_crc.append(realByte)


            # -----------------------------------------------------------------------
            # - Una volta ricostruidi i bytes origilali,
            # - calcoliamo il CRC sui dati (ovviamento escluso il byte di CRC stesso)
            # -----------------------------------------------------------------------
        CRC_calculated  = _calculateCRC8(payLoad_crc[:-1])

            # ---------------------------------
            # - check CRC (drop STX and ETX)
            # ---------------------------------
        CRC_received    = payLoad_crc[-1]
        payLoad         = payLoad_crc[:-1]

        if fDEBUG:
            print ("    CRC received  : x{0:02X}".format(CRC_received))
            print ("    CRC calculated: x{0:02X}".format(CRC_calculated))
            print ()

        if not CRC_received == CRC_calculated:
            print ('ERROR: Il valore di CRC non coincide')
            print ()
            print ("    CRC received  : x{0:02X}".format(CRC_received))
            print ("    CRC calculated: x{0:02X}".format(CRC_calculated))
            print ()
            return bytearray()

        return payLoad



def _calculateCRC8(byteArray_data, fDEBUG=False):
    crcValue = 0
    for byte in byteArray_data:
        # print ('...{0:02x}'.format(byte))
        if isinstance(byte, str): byte = ord(byte)            # onverte nel valore ascii
        if fDEBUG: print ('byte: int:{0} hex: {0:02x} - crcValue int:{1} hex: {1:02x}'.format(byte, crcValue))
        b2 = byte
        if (byte < 0):
            b2 = byte + 256
        for i in range(8):
            odd = ((b2^crcValue) & 1) == 1
            crcValue >>= 1
            b2 >>= 1
            if (odd):
                crcValue ^= 0x8C # this means crc ^= 140

    return crcValue


# ---------------------------------------------
# -     byte1 = aaaa !aaaa
# -     byte2 = bbbb !bbbb
# -     byte = byte1_HNibble * 16 + byte2_HNibble
# ---------------------------------------------
def combineComplementedByte(byte1, byte2,  fDEBUG=False):
    if isinstance(byte1, str): byte1 = ord(byte1)            # onverte nel valore ascii
    if isinstance(byte2, str): byte2 = ord(byte2)            # onverte nel valore ascii

    if fDEBUG: print ("     complementedData: x{0:02X} + x{1:02X}".format(byte1, byte2), end="")

        # - check first byte
    byte1_HighNibble = (byte1 >> 4) & 0x0F
    byte1_LowNibble = ~byte1 & 0x0F
    if byte1_LowNibble != byte1_HighNibble:
        return None

        # - check second byte
    byte2_HighNibble = (byte2 >> 4) & 0x0F
    byte2_LowNibble = ~byte2 & 0x0F
    if byte2_LowNibble != byte2_HighNibble:
        return None

        # re-build real byte
    realByte = byte1_HighNibble*16 + byte2_HighNibble
    if fDEBUG: print ("    -   resulting data BYTE: x{0:02X} char:{1}".format(realByte, chr(realByte)))
    return realByte


# ---------------------------------------------
# - aaaa bbbb
# -     byte1 = aaaa !aaaa
# -     byte2 = bbbb !bbbb
# -     byte = byte1_HNibble * 16 + byte2_HNibble
# ---------------------------------------------
def splitComplementedByte(byte, fDEBUG=False):
    thisFunc = __name__.split('.')[-1]
    if isinstance(byte, str):
        byte = ord(byte)            # onverte nel valore ascii

    logger.debug ("[{0}] -  converting: x{1:02X}".format(thisFunc, byte))
    # if fDEBUG: print ("[{0}] -  converting: x{1:02X}".format(thisFunc, byte))

    # first nibble
    c = byte >> 4;
    byteValue = (c << 4) | (c ^ 0x0F)
    highNibble = byteValue
    logger.debug  ("               x{0:02X}".format( highNibble))

    # second nibble
    c = byte & 0x0F;
    byteValue = (c << 4) | (c ^ 0x0F)
    lowNibble = byteValue
    logger.debug  ("               x{0:02X}".format(lowNibble))



    return highNibble, lowNibble












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
            while True:
                retData = LnRs485_Monitor(port, eod=EOD, fDEBUG=False)
                print ('received: Hex      {0}'.format(' '.join('{0:02x}'.format(x) for x in retData)))
                print ('          Chr      {0}'.format(' '.join('{0:>2}'.format(chr(x)) for x in retData)))
                print()

        elif what in ['rline']:
            port = openRs232Port(portNO, baudRate=9600)
            readLine(port, eol=EOD)

        elif what in ['wline']:
            port = openRs232Port(portNO, baudRate=9600)
            writeLine(port, data='Invio dati....')

        elif what in ['rdata']:
            port = openRs232Port(portNO, baudRate=9600)
            while True:
                retData = readDataInt(port, fPRINT=False, eod=EOD)
                print ('received:       {0}'.format(' '.join('{:02x}'.format(x) for x in retData)))



        else:
            print (Syntax)

    else:
        print (Syntax)


    sys.exit()

