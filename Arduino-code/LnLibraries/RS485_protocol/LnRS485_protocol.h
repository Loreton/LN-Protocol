#if not defined I_AM_RS485_PROTOCOL_H

    #define I_AM_RS485_PROTOCOL_H
    #if defined(ARDUINO) && ARDUINO >= 100
      #include "Arduino.h"
    #else
      #include "WConstants.h"
    #endif



    #if not defined LN_RCV_OK
        #define LN_RCV_OK          0
        #define LN_RCV_OVERFLOW    1
        #define LN_RCV_BADCRC      2
        #define LN_RCV_BADCHAR     3
        #define LN_RCV_TIMEOUT     4
        #define LN_RCV_ERR_TEST   99
        #define MAX_BUFF_SIZE     50
        // const char *rs485ErrMsg[] = {"", "OVERFLOW","BAD-CRC","BAD-CHAR","TIMEOUT"};
    #endif




    // the data we broadcast to each other device
    typedef struct  {
        const byte      dataBuffSize                = MAX_BUFF_SIZE;
        byte            data[MAX_BUFF_SIZE];
        byte            dataCounter                 = 0;    // bytes ricevuti o da trasmettere

        byte            rawData[MAX_BUFF_SIZE];
        byte            rawCounter                  = 0; // bytes ricevuti

        unsigned long   timeout                     = 0;        // send/receive timeout
        byte            fDEBUG                      = false;
        byte            rCode                       = 0;
        // char           *errMsg;

    }  RXTX_DATA, *pRXTX_DATA;




    typedef void (*WriteCallback)  (const byte what);   // send a byte to serial port
    typedef int  (*AvailableCallback)  ();              // return number of bytes available
    typedef int  (*ReadCallback)  ();                   // read a byte from serial port

    void sendMsg (WriteCallback fSend,
                  const byte * data,
                  const byte length,
                  byte *DEBUG_TxRxMsg=NULL);

    byte recvMsg (  AvailableCallback fAvailable,
                    ReadCallback fRead,
                    RXTX_DATA *rxData);

#endif