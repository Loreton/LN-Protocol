/*
 RS485 protocol library.

    reviewed:  Loreto notarantonio
    Version:   LnVer_2017-11-29_19.59.33

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

#include <LnFunctions.h>            // per printHex o altro
#include "LnRS485_protocol.h"

#define CRC_DEBUGxxx // debug in caso di errore del CRC


// calculate 8-bit CRC
static byte crc8(const char *data, byte len) {
    byte crc = 0, i;
    #if defined CRC_DEBUG
        Serial.print( "data len: ");Serial.print(len);Serial.println( );
    #endif

    for (byte index=0; index<len; index++) {
        byte inbyte = data[index];

        #if defined CRC_DEBUG
            Serial.print( "[");Serial.print(index);Serial.print( "] - ");
            printHexPDS( "inbyte: ", inbyte);
            // Serial.print(F("inbyte: "));Serial.print(D2X(inbyte, 2));
            // Serial.print(joinStr("[", Utoa(index, 3, '0'), "] - inbyte: ",D2X(inbyte, 2),  NULL));

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
void sendComplemented (WriteCallback fSend, const byte what, RXTX_DATA *pData) {
byte c, sentByte;

    // high nibble
    c = what >> 4;
    sentByte = (c << 4) | (c ^ 0x0F);
    fSend (sentByte);
    pData->raw[++pData->raw[pDATALEN]] = sentByte;

    // low nibble
    c = what & 0x0F;
    sentByte = (c << 4) | (c ^ 0x0F);
    fSend (sentByte);
    pData->raw[++pData->raw[pDATALEN]] = sentByte;



}  // end of sendComplemented

// ###########################################################
// - il primo byte di pData->tx è la lunghezza dei dati.
// ###########################################################
void sendMsg (RXTX_DATA *pData, WriteCallback fSend) {
    const char LN_SEND_CALLER_DATA[] = "TX-lib";
    // const char LN_SEND_CALLER_RAW[]  = "libSEND-raw ";
    byte txLen = pData->tx[pDATALEN];
    // CRC8calc = 0;

    byte CRC8calc = crc8((char *) &pData->tx[1], txLen);   // calcoliamo il CRC
    pData->Tx_CRCcalc = CRC8calc;
    // printHexPDS( "calculated CRC2: ", CRC8calc, "\n");
    pData->raw[pDATALEN] = 0;
    // pMyID = pData->myID;

    fSend (STX); pData->raw[++pData->raw[pDATALEN]] = STX;

    for (byte i=1; i<=txLen; i++)
        sendComplemented (fSend, pData->tx[i], pData);

    sendComplemented (fSend, CRC8calc, pData);

    fSend (ETX); pData->raw[++pData->raw[pDATALEN]] = ETX;

    if (pData->fDisplayMyData) {
        // printHexPDS( "calculated CRC3: ", pData->Tx_CRCcalc, "\n");
        displayMyData(LN_SEND_CALLER_DATA,  LN_OK, pData);
        // printHexPDS( "calculated CRC4: ", pData->Tx_CRCcalc, "\n");
    }

}  // end of sendMsg


// ###########################################################
// - receive a message, maximum "length" bytes, timeout after "timeout" milliseconds
// - if nothing received, or an error (eg. bad CRC, bad data) return 0
// - if nothing received, or an error (eg. bad CRC, bad data) return 1 (by Loreto per fare comunque il display dei dati ricevuti)
// - otherwise, returns length of received data
// ###########################################################
byte recvMsg (RXTX_DATA *pData,
                ReadCallback fRead,              // read one byte
                AvailableCallback fAvailable)   // return available count
                {

    bool have_stx   = false;
    // const char LN_RECV_CALLER_RAW[]  = "libRECV-raw ";
    const char LN_RECV_CALLER_DATA[] = "RX-data";

    byte dataLen;
    byte lowNibble ;
    byte highNibble ;
    byte CRC8rcvd;
    byte CRC8calc;

    byte maxBuffSize    = sizeof(pData->raw);
    byte unexpextedCounter = 0;
    // pMyID = pData->myID;

    unsigned long start_time = millis();
    pData->raw[pDATALEN] = 0;            // azzeramento dataLen
    pData->rx[pDATALEN] = 0;            // azzeramento dataLen
    while ((millis() - start_time) < pData->timeout) {
        if (fAvailable () > 0) {
            byte inByte = fRead();

              // keep adding if not full
            if (pData->raw[pDATALEN] < maxBuffSize)
                pData->raw[++pData->raw[pDATALEN]] = inByte;    // save byte
            else {
                if (pData->fDisplayMyData) displayMyData(LN_RECV_CALLER_DATA,  LN_OVERFLOW, pData);
                return LN_OVERFLOW;  // overflow
            }


            switch (inByte) {

                case STX:   // start of text
                    have_stx      = true;
                    pData->raw[pDATALEN] = 1;            // azzeramento dataLen
                    start_time    = millis();  // reset timeout period
                    break;




                case ETX:   // end of text - ho tutti i dati nel rawBuffer

                    dataLen = 0;
                        // loop partendo dal byte 2 [byte[0]=len, byte[1]=STX) e finendo prima dell'ETX
                    for (byte i=2; i<pData->raw[pDATALEN]; i+=2) {
                        highNibble          = pData->raw[i] & 0xF0;              // get high-order nibble
                        lowNibble           = pData->raw[i+1] >>4;               // get low-order nibble and join byte
                        pData->rx[++dataLen]  = highNibble | lowNibble;    // inserimento nel buffer dei dati


                        #if defined CRC_DEBUG
                            printHexPDS( "byte0   : ",       pData->raw[i]);
                            printHexPDS( "byte1   : ",       pData->raw[i+1]);
                            printHexPDS( "      byteR   : ", pData->rx[dataLen-1]);
                        #endif
                    }
                    // dataLen--;

                        // --- CRC è l'ultimo byte prima dell'ETX
                    CRC8rcvd = pData->rx[dataLen];
                    pData->Rx_CRCrcvd = CRC8rcvd;

                    pData->rx[pDATALEN] = dataLen-1;       // lunghezza dati ricevuti (esclude CRC byte)

                    // --- calcolo del CRC escludendo il byte di CRC precedentemente salvato
                    CRC8calc = crc8((char *) &pData->rx[1], pData->rx[pDATALEN]);
                    pData->Rx_CRCcalc = CRC8calc;


                    #if defined CRC_DEBUG
                        Serial.print( "dataLen : ");Serial.println(pData->rx[pDATALEN]);
                        printHexPDS(  "CRC8rcvd: ", CRC8rcvd);
                        printHexPDS(  "CRC8calc: ", CRC8calc);
                    #endif


                    if (CRC8calc != CRC8rcvd) {
                        if (pData->fDisplayMyData) displayMyData(LN_RECV_CALLER_DATA,  LN_BADCRC, pData);
                        return LN_BADCRC;  // bad crc
                    }

                    if (pData->fDisplayMyData) {
                        Serial.print("\r\n\r\n");
                        displayMyData(LN_RECV_CALLER_DATA, LN_OK, pData);
                    }
                    return LN_OK;






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
                        --pData->raw[pDATALEN]; // decrease rawLen

                    break;

                default:
                    --pData->raw[pDATALEN]; // decrease rawLen

                    if (unexpextedCounter == 0) {
                        if (pData->fDisplayMyData) {
                            Serial.println();
                            Serial.print(pData->myID);
                            printHexPDS("libRECV - unexpexted byte(s): ", inByte, "");
                        }
                    }

                    if (pData->fDisplayMyData) printHexPDS(" ", inByte, "");

                    // printHex(inByte);
                    unexpextedCounter++;
                    break;

            }  // end of switch
        }  // end of incoming data
    } // end of while not timed out2

    // Serial.println();
    if (pData->fDisplayMyData) displayMyData(LN_RECV_CALLER_DATA, LN_TIMEOUT, pData);


    return LN_TIMEOUT;  // timeout

} // end of recvMsg


