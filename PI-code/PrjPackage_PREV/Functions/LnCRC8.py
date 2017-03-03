#!/usr/bin/env python3


# http://www.evilgeniuslair.com/2015/01/14/crc-8/

import binascii

def strCheckSum(strData):
    bytes_data      = strData.encode()
    bytes_hex_data  = binascii.hexlify(bytes_data)
    byteArray_data  = bytearray(bytes_hex_data)
    result = calculateCRC8(byteArray_data)
    return result

def hexCheckSum(hexData):
    print (type(hexData), hexData)
    bytes_hex_data = hexData.encode()
    byteArray_data = bytearray(bytes_hex_data)
    result = calculateCRC8(byteArray_data)
    return result

def byteArrayCheckSum(byteArray_data):
    result = calculateCRC8(byteArray_data)
    return result

def calculateCRC8(byteArray_data):
    result = 0
    for byte in byteArray_data:
        # print ('byte: {0} - result {1}'.format( byte, result))
        b2 = byte
        if (byte < 0):
            b2 = byte + 256
        for i in range(8):
            odd = ((b2^result) & 1) == 1
            result >>= 1
            b2 >>= 1
            if (odd):
                result ^= 0x8C # this means crc ^= 140

    return result


if __name__ == '__main__':
    import sys

    msg = bytearray(3)
    msg[0] = 1
    msg[1] = 2
    msg[2] = 0xcb   # ATTESO D0 come CRC8

    if isinstance(msg, bytearray):
        CRC8 = byteArrayCheckSum(msg)
        print ("CRC-8 Maxim/Dallas: {0} ".format(hex(CRC8)))


    msg = sys.argv[1]
    if isinstance(msg, str):
        # interpretato com STRING value
        CRC8 = strCheckSum(msg)
        print ("CRC-8 Maxim/Dallas: {0} ".format(hex(CRC8)))
        # interpretato com HEX value
        # CRC8 = calcCheckSum(hexData=msg)
        CRC8 = hexCheckSum(msg)
        print ("CRC-8 Maxim/Dallas: {0} ".format(hex(CRC8)))
