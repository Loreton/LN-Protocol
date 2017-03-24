/*
 RS485 protocol library.

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

#include <LnFunctions.h>                    // for SET_CRC_BEFORE_ETX definition
#include "LnRS485_protocol.h"

// const byte STX = '\02';
// const byte ETX = '\03';
const byte STX = 0x02;
const byte ETX = 0x03;
// byte fDEBUG     = false;

const bool  SET_CRC_BEFORE_ETX = true;    // by Loreto


// calculate 8-bit CRC
static byte crc8(const byte *addr, byte len) {
    byte crc = 0;
    while (len--) {
        byte inbyte = *addr++;
        for (byte i = 8; i; i--) {
            byte mix = (crc ^ inbyte) & 0x01;
            crc >>= 1;
            if (mix)
                crc ^= 0x8C;
            inbyte >>= 1;
        }  // end of for
    }  // end of while
    return crc;
}  // end of crc8

// ###########################################################
// - send a byte complemented, repeated
// - only values sent would be (in hex):
// -   0F, 1E, 2D, 3C, 4B, 5A, 69, 78, 87, 96, A5, B4, C3, D2, E1, F0
// -   invia prima l'HighNibble e poi il LowNibble
// ###########################################################
void sendComplemented (WriteCallback fSend, const byte what) {
byte c;

    // first nibble
    c = what >> 4;
    fSend ((c << 4) | (c ^ 0x0F));

    // second nibble
    c = what & 0x0F;
    fSend ((c << 4) | (c ^ 0x0F));

}  // end of sendComplemented

// ###########################################################
// - il primo byte di pTx->data è la lunghezza dei dati.
// ###########################################################
void sendMsg (WriteCallback fSend, RXTX_DATA *pTx) {
    byte dataLen = pTx->data[0];

    byte CRC8value = crc8(&pTx->data[1], dataLen);   // calcoliamo il CRC

    fSend (STX);  // STX

    for (byte i = 1; i < dataLen; i++) {
        sendComplemented (fSend, pTx->data[i]);
        // pTx->rawData[++TxCount] = pTx->data[i];         // by Loreto
    }

    sendComplemented (fSend, CRC8value);  // by Loreto - inserito prima del ETX
    fSend (ETX);

}  // end of sendMsg


// ###########################################################
// - receive a message, maximum "length" bytes, timeout after "timeout" milliseconds
// - if nothing received, or an error (eg. bad CRC, bad data) return 0
// - if nothing received, or an error (eg. bad CRC, bad data) return 1 (by Loreto per fare comunque il display dei dati ricevuti)
// - otherwise, returns length of received data
// ###########################################################
byte recvMsg (AvailableCallback fAvailable,   // return available count
              ReadCallback fRead,             // read one byte
              RXTX_DATA *pRx) {

    bool have_stx   = false;


    // variables below are set when we get an STX

    bool first_nibble;
    byte current_byte;


    byte CRC8calc ;
    byte CRC8rcvd ;

    byte rawCounter  = 0;
    byte dataCounter = 0;
    byte buffSize    = sizeof(pRx->data);
    pRx->data[0]     = dataCounter;   // inizializziamo counter
    pRx->rawData[0]  = rawCounter;   // inizializziamo counter

    // Serial.print("\r\ndata        size: ");Serial.println(sizeof(pRx->data));
    // Serial.print("rawData size: ");Serial.println(sizeof(pRx->rawData));

    unsigned long start_time = millis();

    while ((millis() - start_time) < pRx->timeout) {
        if (fAvailable () > 0) {
            byte inByte = fRead();
            pRx->rawData[++rawCounter] = inByte;         // by Loreto
            pRx->rawData[0] = rawCounter;                   // update counter

            switch (inByte) {

                case STX:   // start of text
                    have_stx        = true;
                    dataCounter     = 0;        // azzeriamo counter
                    first_nibble    = true;
                    start_time      = millis();  // reset timeout period
                    break;

                case ETX:   // end of text
                    /*
                        il byte precedente dovrebbe essere il CRC.
                        verifichiamo che sia valido.
                    */

                    // --- CRC dovrebbe essere l'ultimo byte prima dell'ETX
                    CRC8rcvd = pRx->data[dataCounter];

                    // --- calcolo del CRC senza il CRC e senza il byte[0]--> datacounter
                    CRC8calc = crc8(&pRx->data[1], dataCounter-1);
                    pRx->data[0]--;
                    if (CRC8calc != CRC8rcvd)
                        return LN_RCV_BADCRC;  // bad crc
                    else
                        return LN_RCV_OK;



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

                      // shift a dx
                    inByte >>= 4;

                      // save high-order nibble...
                    if (first_nibble) {
                        current_byte = inByte;
                        first_nibble = false;
                        break;
                    }  // end of first nibble


                    // get low-order nibble and join byte
                    current_byte <<= 4;
                    current_byte |= inByte;
                    first_nibble = true;
                    // printHexPDS( "      current_byte: ", current_byte);

                      // keep adding if not full
                    if (dataCounter < buffSize) {
                        pRx->data[++dataCounter] = current_byte;    // save byte
                        pRx->data[0] = dataCounter;                 // update counter
                    }
                    else {
                        return LN_RCV_OVERFLOW;  // overflow
                    }

                    break;

                default:
                    printHexPDS("unexpexted byte: ", inByte);
                    break;

            }  // end of switch
        }  // end of incoming data
    } // end of while not timed out2

    return LN_RCV_TIMEOUT;  // timeout

} // end of recvMsg

