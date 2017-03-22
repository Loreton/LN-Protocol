#if not defined I_AM_RS485_PROTOCOL_H

    #define I_AM_RS485_PROTOCOL_H
    #if defined(ARDUINO) && ARDUINO >= 100
      #include "Arduino.h"
    #else
      #include "WConstants.h"
    #endif

    #define MAX_MSG_SIZE2            50

    // the data we broadcast to each other device
    typedef struct  {
        byte sourceAddress;
        byte destAddress;
        byte data[MAX_MSG_SIZE2];
        byte debugData[MAX_MSG_SIZE2];
        const byte buffLen = MAX_MSG_SIZE2;
        unsigned long timeout = 0;
        byte fDEBUG = false;
    }  RXTX_DATA, *pRXTX_DATA;




    typedef void (*WriteCallback)  (const byte what);   // send a byte to serial port
    typedef int  (*AvailableCallback)  ();              // return number of bytes available
    typedef int  (*ReadCallback)  ();                   // read a byte from serial port

    void sendMsg (WriteCallback fSend,
                  const byte * data,
                  const byte length,
                  byte *DEBUG_TxRxMsg=NULL);

    byte recvMsg_OK (AvailableCallback fAvailable, ReadCallback fRead,
                  byte * data,
                  const byte length,
                  unsigned long timeout,   // come default aveva = 500 by Loreto
                  byte *DEBUG_TxRxMsg=NULL);

    byte recvMsg (  AvailableCallback fAvailable,
                    ReadCallback fRead,
                    RXTX_DATA *rxData);
                    // byte * data,
                    // const byte length,
                    // unsigned long timeout,   // come default aveva = 500 by Loreto
                    // byte *DEBUG_TxRxMsg,

#endif