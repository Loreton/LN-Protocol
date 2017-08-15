#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

def displayRawData(rawData):
    if len(rawData):
        COMMAND_DATA = 7    # TX - dati necessari al comando per la sua corretta esecuzione/RX - dati di risposta
        print ('    full data - len: [{0:03}] - '.format(len(rawData)), end="")
        for byte in rawData: print ('{0:02X} '.format(byte), end="")
        print ()
        print ()
        commandData = rawData[COMMAND_DATA*2:]
        print ('    raw data - len: [{0:03}] - '.format(len(commandData)), end="")
        print ('   '*COMMAND_DATA, end="")
        print ('[', end="")
        printableChars = list(range(31,126))
        printableChars.append(13)
        printableChars.append(10)
        for byte in rawData:
            if byte in printableChars:   # Handle only printable ASCII
                print(chr(byte), end="")
            else:
                print(' ', end="")
    else:
        print('No data received!')
