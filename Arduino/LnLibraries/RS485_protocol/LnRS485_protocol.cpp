/*
 RS485 protocol library.

    reviewed:  Loreto notarantonio
    Version:   LnVer_2017-04-07_16.50.59

     Devised and written by Nick Gammon.
     Date: 14 November 2011
     Version: 1.1


     Version 1.1 reset the timeout period after getting STX.

     Licence: Released for public use.


     Can send from 1 to 255 bytes from one node to another with:

     * Packet start indicator (STX)
     * Each data byte is doubled and inverted to check validity
     * Packet end indicator (ETX)
     * Packet CRC (checksum)

    Modifiche di Loreto:
        - Spostato il CRC prima del byte di ETX
        - inserita la variabile DEBUG_TxData per ritornare il messaggio ricevuto oppure trasmesso e verificarne il contenuto.
          Anche il valore di ritorno è stato portato da 0 ad 1 per permettere di analizzare il contenuto.


     To allow flexibility with hardware (eg. Serial, SoftwareSerial, I2C)
     you provide three "callback" functions which send or receive data. Examples are:

     void fWrite (const byte what)
     {
     Serial.write (what);
     }

     int fAvailable ()
     {
     return Serial.available ();
     }

     int fRead ()
     {
     return Serial.read ();
     }

 */

#define I_AM_RS485_PROTOCOL_CPP

#include <LnFunctions.h>
#include "LnRS485_protocol.h"

#define xxxCRC_DEBUG // debug in caso di errore del CRC

const byte STX = 0x02;
const byte ETX = 0x03;


const char *errMsg[]    = { " - OK      ",
                            " - OVERFLOW",
                            " - BAD-CRC ",
                            " - BAD-CHAR",
                            " - TIMEOUT ",
                            " - PAYLOAD ",
                            " - DEBUG   ",
                        };
// calculate 8-bit CRC
static byte crc8(const byte *data, byte len) {
    byte crc = 0, i;
    #if defined CRC_DEBUG
        Serial.print( "data len: ");Serial.print(len);Serial.println( );
    #endif

    for (byte index=0; index<len; index++) {
        byte inbyte = data[index];

        #if defined CRC_DEBUG
            Serial.print( "[");Serial.print(index);Serial.print( "] - ");
            printHexPDS( "inbyte: ", inbyte);
        #endif

        for (i = 8; i; i--) {
            byte mix = (crc ^ inbyte) & 0x01;
            crc >>= 1;
            if (mix)
                crc ^= 0x8C;
            inbyte >>= 1;
        }  // end of for
    }

    #if defined CRC_DEBUG
        printHexPDS( "calculated CRC: ", crc);
        Serial.println();
    #endif

    return crc;
}



// ###########################################################
// - send a byte complemented, repeated
// - only values sent would be (in hex):
// -   0F, 1E, 2D, 3C, 4B, 5A, 69, 78, 87, 96, A5, B4, C3, D2, E1, F0
// -   invia prima l'HighNibble e poi il LowNibble
// ###########################################################
void sendComplemented (WriteCallback fSend, const byte what, RXTX_DATA *ptrData) {
byte c, sentByte;

    // high nibble
    c = what >> 4;
    sentByte = (c << 4) | (c ^ 0x0F);
    fSend (sentByte);
    ptrData->raw[++ptrData->raw[0]] = sentByte;

    // low nibble
    c = what & 0x0F;
    sentByte = (c << 4) | (c ^ 0x0F);
    fSend (sentByte);
    ptrData->raw[++ptrData->raw[0]] = sentByte;


}  // end of sendComplemented

// ###########################################################
// - il primo byte di ptrData->tx è la lunghezza dei dati.
// ###########################################################
void sendMsg (WriteCallback fSend, RXTX_DATA *ptrData) {
    const char LN_SEND_CALLER_DATA[] = "libSEND-data";
    const char LN_SEND_CALLER_RAW[]  = "libSEND-raw ";
    byte CRC8value = crc8(&ptrData->tx[1], ptrData->tx[0]);   // calcoliamo il CRC
    ptrData->raw[0] = 0;


    fSend (STX);  // STX
    ptrData->raw[++ptrData->raw[0]] = STX;

    for (byte i=1; i<=ptrData->tx[0]; i++)
        sendComplemented (fSend, ptrData->tx[i], ptrData);


    sendComplemented (fSend, CRC8value, ptrData);

    fSend (ETX);
    ptrData->raw[++ptrData->raw[0]] = ETX;

    if (ptrData->displayData) {
        displayDebugMessage(LN_SEND_CALLER_RAW,  LN_OK, ptrData->raw);
        displayDebugMessage(LN_SEND_CALLER_DATA, LN_OK, ptrData->tx);
    }

}  // end of sendMsg


// ###########################################################
// - receive a message, maximum "length" bytes, timeout after "timeout" milliseconds
// - if nothing received, or an error (eg. bad CRC, bad data) return 0
// - if nothing received, or an error (eg. bad CRC, bad data) return 1 (by Loreto per fare comunque il display dei dati ricevuti)
// - otherwise, returns length of received data
// ###########################################################
byte recvMsg (AvailableCallback fAvailable,   // return available count
              ReadCallback fRead,             // read one byte
              RXTX_DATA *ptrData) {

    bool have_stx   = false;
    const char LN_RECV_CALLER_RAW[]  = "libRECV-raw ";
    const char LN_RECV_CALLER_DATA[] = "libRECV-data";

    // variables below are set when we get an STX

    bool first_nibble;
    byte current_byte;


    byte CRC8calc ;
    byte CRC8rcvd ;
    byte lowNibble ;
    byte highNibble ;

    byte buffSize    = sizeof(ptrData->rx);

    unsigned long start_time = millis();
    ptrData->raw[0] = 0;            // azzeramento dataLen
    while ((millis() - start_time) < ptrData->timeout) {
        if (fAvailable () > 0) {
            byte inByte = fRead();
            ptrData->raw[++ptrData->raw[0]] = inByte;         // by Loreto

            switch (inByte) {

                case STX:   // start of text
                    have_stx        = true;
                    ptrData->rx[0]    = 0;            // azzeramento dataLen
                    // ptrData->raw[0] = 0;            // azzeramento dataLen
                    first_nibble    = true;
                    start_time      = millis();  // reset timeout period
                    break;

                case ETX:   // end of text

                    // --- CRC è l'ultimo byte prima dell'ETX
                    CRC8rcvd = ptrData->rx[ptrData->rx[0]];

                    // --- calcolo del CRC escludendo il byte di CRC precedentemente salvato
                    CRC8calc = crc8(&ptrData->rx[1], --ptrData->rx[0]);

                    #if defined CRC_DEBUG
                        Serial.print( "dataLen : ");Serial.println(ptrData->rx[0]);
                        printHexPDS( "CRC8rcvd: ", CRC8rcvd);
                        printHexPDS( "CRC8calc: ", CRC8calc);
                    #endif


                    if (CRC8calc != CRC8rcvd) {
                        displayDebugMessage(LN_RECV_CALLER_RAW,  LN_BADCRC, ptrData->raw);
                        displayDebugMessage(LN_RECV_CALLER_DATA, LN_BADCRC, ptrData->rx);
                        return LN_BADCRC;  // bad crc
                    }
                    else {
                        if (ptrData->displayData) {
                            displayDebugMessage(LN_RECV_CALLER_RAW, LN_OK, ptrData->raw);
                            displayDebugMessage(LN_RECV_CALLER_DATA,    LN_OK, ptrData->rx);
                        }
                        return LN_OK;
                    }

                case 0x0F:
                case 0x1E:
                case 0x2D:
                case 0x3C:
                case 0x4B:
                case 0x5A:
                case 0x69:
                case 0x78:
                case 0x87:
                case 0x96:
                case 0xA5:
                case 0xB4:
                case 0xC3:
                case 0xD2:
                case 0xE1:
                case 0xF0:
                    if (!have_stx)
                      break;

                      // save high-order nibble...
                    if (first_nibble) {
                        highNibble = inByte & 0xF0;
                        first_nibble = false;
                        break;
                    }

                    // get low-order nibble and join byte
                    lowNibble    = inByte >>4;
                    current_byte = highNibble | lowNibble;
                    first_nibble = true;


                      // keep adding if not full
                    if (ptrData->rx[0] < buffSize)
                        ptrData->rx[++ptrData->rx[0]] = current_byte;    // save byte
                    else {
                        displayDebugMessage(LN_RECV_CALLER_RAW,  LN_OVERFLOW, ptrData->raw);
                        displayDebugMessage(LN_RECV_CALLER_DATA, LN_OVERFLOW, ptrData->rx);
                        return LN_OVERFLOW;  // overflow
                    }


                    break;

                default:
                    printHexPDS("unexpexted byte: ", inByte);
                    break;

            }  // end of switch
        }  // end of incoming data
    } // end of while not timed out2

    displayDebugMessage(LN_RECV_CALLER_RAW, LN_TIMEOUT, ptrData->raw);
    displayDebugMessage(LN_RECV_CALLER_DATA, LN_TIMEOUT, ptrData->rx);

    return LN_TIMEOUT;  // timeout

} // end of recvMsg


// #############################################################
// # const char* text : per ricevere una stringa constante es: "Loreto"
// #############################################################
void displayDebugMessage(const char *caller, byte rCode, const byte *data) {
    byte dataLen = data[0];
    Serial.print(caller);
    Serial.print(errMsg[rCode]);
    Serial.print(F("   ("));Serial.print(LnUtoa(dataLen, 3, ' '));Serial.print(F(") - "));
    if (dataLen > 0)
        printHex(&data[1], dataLen);

    return;
}



#if 0
// #############################################################
// # const char* text : per ricevere una stringa constante es: "Loreto"
// #############################################################
void displayData(void) {
    byte dataLen = myRawData[0];

    Serial.print(F(" raw->  ("));Serial.print(dataLen);Serial.print(F(") - "));
    if (dataLen > 0)
        printHex(&myRawData[1], dataLen); // contiene LEN STX ...data... ETX


    return;
}

// #############################################################
// #
// #############################################################
void printPayload(RXTX_DATA *ptr) {
    byte dataLen = ptrData->data[0];
    Serial.print(F(" ptrData-> ("));Serial.print(ptrData->data[0]);Serial.print(F(") - "));
    if (dataLen > 0)
        printHex(&ptrData->data[1], ptrData->data[0], "\r\n");

    return;
}

// #############################################################
// # const char* text : per ricevere una stringa constante es: "Loreto"
// #############################################################
void printData(void) {
    byte dataLen = myRawData[0];

    if (dataLen > 0) {
        Serial.print(F(" raw-> ("));Serial.print(dataLen);Serial.print(F(") - "));
        printHex(&myRawData[1], dataLen); // contiene LEN STX ...data... ETX
    }

    return;
}
#endif