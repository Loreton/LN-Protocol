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
static byte crc8 (const byte *addr, byte len) {
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

// send a byte complemented, repeated
// only values sent would be (in hex):
//   0F, 1E, 2D, 3C, 4B, 5A, 69, 78, 87, 96, A5, B4, C3, D2, E1, F0
//   invia prima l'HighNibble e poi il LowNibble
void sendComplemented (WriteCallback fSend, const byte what) {
byte c;

    // first nibble
    c = what >> 4;
    fSend ((c << 4) | (c ^ 0x0F));

    // second nibble
    c = what & 0x0F;
    fSend ((c << 4) | (c ^ 0x0F));

}  // end of sendComplemented

// send a message of "length" bytes (max 255) to other end
// put STX at start, ETX at end, and add CRC
void sendMsg (WriteCallback fSend, const byte * data, const byte length, byte *DEBUG_TxData) {
    byte fDEBUG = false;
    byte TxCount = 0;

    if (DEBUG_TxData[0] == 255) {
        fDEBUG = false;
    }
    else {
        fDEBUG = true;
        DEBUG_TxData[++TxCount] = STX;         // by Loreto
        Serial.println("\r\n\r\n...siamo in Tx-DEBUG mode!");
    }

    byte CRC8value = crc8 (data, length);       // by Loreto

    fSend (STX);  // STX

    for (byte i = 0; i < length; i++) {
        sendComplemented (fSend, data [i]);
        if (fDEBUG) DEBUG_TxData[++TxCount] = data[i];         // by Loreto
    }

    if (SET_CRC_BEFORE_ETX == true) {
        sendComplemented (fSend, CRC8value);  // by Loreto - inserito prima del ETX
        if (fDEBUG) DEBUG_TxData[++TxCount] = CRC8value;       // by Loreto
        fSend (ETX);
        if (fDEBUG) DEBUG_TxData[++TxCount] = ETX;             // by Loreto
    } else {
        fSend (ETX);
        if (fDEBUG) DEBUG_TxData[++TxCount] = ETX;             // by Loreto
        sendComplemented (fSend, CRC8value);
        if (fDEBUG) DEBUG_TxData[++TxCount] = CRC8value;       // by Loreto
    }
    if (fDEBUG) DEBUG_TxData[0] = TxCount;                 // by Loreto (dovrebbe contenere: LEN(escluso byt0) STX ...data... CRC ETX)


}  // end of sendMsg


// receive a message, maximum "length" bytes, timeout after "timeout" milliseconds
// if nothing received, or an error (eg. bad CRC, bad data) return 0
// if nothing received, or an error (eg. bad CRC, bad data) return 1 (by Loreto per fare comunque il display dei dati ricevuti)
// otherwise, returns length of received data
byte recvMsg (AvailableCallback fAvailable,   // return available count
              ReadCallback fRead,             // read one byte
              RXTX_DATA *pRx) {

    byte RxCount = 0;
    bool have_stx = false;

    if (pRx->fDEBUG == true) {
        pRx->debugData[0] = 0;     // initialize il counter a 0
        Serial.println("\r\n\r\n...siamo in Rx-DEBUG mode!");
    }


    // variables below are set when we get an STX
    bool have_etx;
    byte input_pos;
    bool first_nibble;
    byte current_byte;


    unsigned long start_time = millis();
    while ((millis() - start_time) < pRx->timeout) {
        if (fAvailable () > 0) {
            byte inByte = fRead();

            if (pRx->fDEBUG) {
                pRx->debugData[++RxCount] = inByte;         // by Loreto
                printHexPDS("received: ", inByte);
            }
            switch (inByte) {

                case STX:   // start of text
                    have_stx     = true;
                    have_etx     = false;
                    input_pos    = 0;
                    first_nibble = true;
                    start_time   = millis();  // reset timeout period
                    break;

                case ETX:   // end of text
                    if (SET_CRC_BEFORE_ETX == true) {
                        /*
                            il byte precedente dovrebbe essere il CRC.
                            verifichiamo che sia valido.
                        */
                        byte CRCpos   = input_pos;      // dovrebbe puntare al CRC
                        byte CRC8calc = crc8(pRx->data, input_pos-1); // verificato
                        byte CRC8rcvd = pRx->data[CRCpos-1];

                        if (pRx->fDEBUG) pRx->debugData[0] = RxCount;                 // by Loreto (dovrebbe contenere: LEN(escluso byt0) STX ...data... CRC ETX)
                        if (CRC8calc != CRC8rcvd)
                            return LN_RCV_BADCRC;  // bad crc
                        return input_pos-1;  // return received length escludendo il byte di CRC

                    } else {
                        have_etx = true;
                        break;
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

                    // check byte is in valid form (4 bits followed by 4 bits complemented)
                    // non c'è ragione in quanto appartiene sicuramente ad uno dei byte del case-
                    if ((inByte >> 4) != ((inByte & 0x0F) ^ 0x0F) )
                        return LN_RCV_BADCHAR;  // bad character

                      // convert back
                    inByte >>= 4;

                      // high-order nibble?
                    if (first_nibble) {
                        current_byte = inByte;
                        first_nibble = false;
                        break;
                    }  // end of first nibble

                    // low-order nibble
                    current_byte <<= 4;
                    current_byte |= inByte;
                    first_nibble = true;

                      // if we have the ETX this must be the CRC
                    if (have_etx) {
                        if (pRx->fDEBUG) pRx->debugData[0] = RxCount;                 // by Loreto (dovrebbe contenere: LEN(escluso byt0) STX ...data... CRC ETX)
                        if (crc8 (pRx->data, input_pos) != current_byte)
                            return LN_RCV_BADCRC;  // bad crc
                        return input_pos;  // return received length
                    }  // end if have ETX already

                      // keep adding if not full
                    if (input_pos < pRx->buffLen)
                        pRx->data[input_pos++] = current_byte;
                    else
                        return LN_RCV_ERROR;  // overflow
                    break;

                default:
                    printHexPDS("unexpexted byte: ", inByte);
                    break;

            }  // end of switch
        }  // end of incoming data
    } // end of while not timed out

    return LN_RCV_TIMEOUT;  // timeout
} // end of recvMsg

#if 0
// receive a message, maximum "length" bytes, timeout after "timeout" milliseconds
// if nothing received, or an error (eg. bad CRC, bad data) return 0
// if nothing received, or an error (eg. bad CRC, bad data) return 1 (by Loreto per fare comunque il display dei dati ricevuti)
// otherwise, returns length of received data
byte recvMsg (AvailableCallback fAvailable,   // return available count
              ReadCallback fRead,             // read one byte
              byte * data,                    // buffer to receive into
              const byte length,              // maximum buffer size
              unsigned long timeout,          // milliseconds before timing out
              byte *DEBUG_RxData) {

    byte RxCount = 0;
    bool have_stx = false;
    byte fDEBUG;

    if (DEBUG_RxData[0] == 255) {
        fDEBUG = false;
    }
    else {
        fDEBUG = true;
        DEBUG_RxData[0] = 0;     // initialize il counter a 0
        Serial.println("\r\n\r\n...siamo in Rx-DEBUG mode!");
        Serial.println(sizeof(DEBUG_RxData));
    }




    // variables below are set when we get an STX
    bool have_etx;
    byte input_pos;
    bool first_nibble;
    byte current_byte;


    unsigned long start_time = millis();
    while ((millis() - start_time) < timeout) {
        if (fAvailable () > 0) {
            byte inByte = fRead();

            if (fDEBUG) {
                DEBUG_RxData[++RxCount] = inByte;         // by Loreto
                printHexPDS("received: ", inByte);
            }
            switch (inByte) {

                case STX:   // start of text
                    have_stx = true;
                    have_etx = false;
                    input_pos = 0;
                    first_nibble = true;
                    start_time = millis();  // reset timeout period
                    break;

                case ETX:   // end of text
                    if (SET_CRC_BEFORE_ETX == true) {
                        /*
                            il byte precedente dovrebbe essere il CRC.
                            verifichiamo che sia valido.
                        */
                        byte CRCpos = input_pos;      // dovrebbe puntare al CRC
                        byte CRC8calc = crc8(data, input_pos-1); // verificato
                        byte CRC8rcvd = data[CRCpos-1];

                        if (fDEBUG) DEBUG_RxData[0] = RxCount;                 // by Loreto (dovrebbe contenere: LEN(escluso byt0) STX ...data... CRC ETX)
                        if (CRC8calc != CRC8rcvd)
                            return LN_RCV_BADCRC;  // bad crc
                        return input_pos-1;  // return received length escludendo il byte di CRC

                    } else {
                        have_etx = true;
                        break;
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

                    // check byte is in valid form (4 bits followed by 4 bits complemented)
                    // non c'è ragione in quanto appartiene sicuramente ad uno dei byte del case-
                    if ((inByte >> 4) != ((inByte & 0x0F) ^ 0x0F) )
                        return LN_RCV_BADCHAR;  // bad character

                      // convert back
                    inByte >>= 4;

                      // high-order nibble?
                    if (first_nibble) {
                        current_byte = inByte;
                        first_nibble = false;
                        break;
                    }  // end of first nibble

                    // low-order nibble
                    current_byte <<= 4;
                    current_byte |= inByte;
                    first_nibble = true;

                      // if we have the ETX this must be the CRC
                    if (have_etx) {
                        if (fDEBUG) DEBUG_RxData[0] = RxCount;                 // by Loreto (dovrebbe contenere: LEN(escluso byt0) STX ...data... CRC ETX)
                        if (crc8 (data, input_pos) != current_byte)
                            return LN_RCV_BADCRC;  // bad crc
                        return input_pos;  // return received length
                    }  // end if have ETX already

                      // keep adding if not full
                    if (input_pos < length)
                        data [input_pos++] = current_byte;
                    else
                        return LN_RCV_ERROR;  // overflow
                    break;

                default:
                    printHexPDS("unexpexted byte: ", inByte);
                    break;

            }  // end of switch
        }  // end of incoming data
    } // end of while not timed out

    return LN_RCV_TIMEOUT;  // timeout
} // end of recvMsg

#endif