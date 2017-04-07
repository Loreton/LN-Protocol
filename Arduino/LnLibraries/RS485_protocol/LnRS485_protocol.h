// ########################################
// Author:  Loreto notarantonio
// Version: LnVer_2017-04-07_16.48.34
// ########################################


#if not defined I_AM_RS485_PROTOCOL_H


    #define I_AM_RS485_PROTOCOL_H
    #if defined(ARDUINO) && ARDUINO >= 100
      #include "Arduino.h"
    #else
      #include "WConstants.h"
    #endif


    // extern enum errorType;
    extern const char *errMsg[];
    // extern const byte LN_SEND_CALLER[];
    // extern const byte LN_RECV_CALLER[];

    #if not defined LN_RCV_OK
    enum errorType  {   LN_OK=0,
                        LN_OVERFLOW,
                        LN_BADCRC,
                        LN_BADCHAR,
                        LN_TIMEOUT,
                        LN_PAYLOAD,
                        LN_DEBUG,
                    };

        #define MAX_DATA_SIZE     20


    #else
    #endif




    // the data we broadcast to each other device
    typedef struct  {
        byte            rx[MAX_DATA_SIZE];        // byte[0] is dataLen
        byte            tx[MAX_DATA_SIZE];        // byte[0] is dataLen
        byte            raw[MAX_DATA_SIZE*2+2];   // byte[0] is dataLen SIZE = dataLen + STX+ETX
        unsigned long   timeout  = 10000;        // send/receive timeout
        byte            displayData = false;        // per fare il print del rawData
    }  RXTX_DATA, *pRXTX_DATA;





    typedef void (*WriteCallback)  (const byte what);   // send a byte to serial port
    typedef int  (*AvailableCallback)  ();              // return number of bytes available
    typedef int  (*ReadCallback)  ();                   // read a byte from serial port



    void sendMsg (WriteCallback fSend,
                  RXTX_DATA *rxData);

    byte recvMsg (  AvailableCallback fAvailable,
                    ReadCallback fRead,
                    RXTX_DATA *rxData);

        // dataLen is byte data[0]
    // void displayDebugMessage(const char *msgText, const byte *data);
    // void displayDebugMessage(byte errMscType, const byte *data);
    // void displayDebugMessage_(byte errMscType, const byte *data);
    void displayDebugMessage(const char *caller, byte errMscType, const byte *data);
    void prova(const char *caller);

#endif