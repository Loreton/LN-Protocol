// ########################################
// Author:  Loreto notarantonio
// Version: LnVer_2017-07-25_17.03.54
// ########################################

#if defined(ARDUINO) && ARDUINO >= 100
    #include "Arduino.h"
#else
    #include "WConstants.h"
#endif


// #if not defined I_AM_RS485_PROTOCOL_H
#if defined I_AM_RS485_PROTOCOL_CPP
    // #define I_AM_RS485_PROTOCOL_H

    const char *errMsg[]    = { "OK",
                                "OVERFLOW",
                                "BAD-CRC",
                                "BAD-CHAR",
                                "TIMEOUT",
                                "PAYLOAD",
                                "DEBUG",
                            };



#else
    extern const char *errMsg[];

#endif

    extern const char TAB[];


    const byte STX    = 0x02;
    const byte ETX    = 0x03;

    const byte ENA_TX = HIGH;
    const byte ENA_RX = LOW;
    const byte DIS_TX = LOW;

    const byte ENA_485_TX = HIGH;
    const byte ENA_485_RX = LOW;


    // #if not defined LN_RCV_OK
        enum errorType  {
                        LN_OK=0,
                        LN_OVERFLOW,
                        LN_BADCRC,
                        LN_BADCHAR,
                        LN_TIMEOUT,
                        LN_PAYLOAD,
                        LN_DEBUG,
                    };

        #define MAX_DATA_SIZE     30
    // definizione messa qui per comodità con  il printMessage.
    enum RXTX_MAP  {
                        DATALEN=0,
                        SENDER_ADDR,
                        DESTINATION_ADDR,
                        SEQNO_HIGH,
                        SEQNO_LOW,
                        CMD_RCODE,
                        COMMAND,
                        SUBCOMMAND,
                        COMMAND_DATA,
                    };

//  identifica il byte che contiene la lunghezza dati
    #define pDATALEN     0

    // the data we broadcast to each other device
    typedef struct  {
        byte            rx[MAX_DATA_SIZE];        // byte[0] is dataLen
        byte            tx[MAX_DATA_SIZE];        // byte[0] is dataLen
        byte            raw[MAX_DATA_SIZE*2+2];   // byte[0] is dataLen SIZE = dataLen + STX+ETX
        unsigned long   timeout         = 10000;        // send/receive timeout
        byte            displayData     = false;     // per fare il print dei data
        byte            displayRawData  = false;     // per fare il print del rawData
        char            *myID;    // pointer identificativo di Arduino
        byte            Tx_CRCcalc;    // CRC value
        byte            Rx_CRCcalc;    // CRC value
        byte            Rx_CRCrcvd;    // CRC value
    }  RXTX_DATA, *pRXTX_DATA;

    typedef void (*WriteCallback)  (const byte what);   // send a byte to serial port
    typedef int  (*AvailableCallback)  ();              // return number of bytes available
    typedef int  (*ReadCallback)  ();                   // read a byte from serial port



    void sendMsg (RXTX_DATA *rxData, WriteCallback fSend);
    byte recvMsg (RXTX_DATA *rxData, ReadCallback fRead, AvailableCallback fAvailable);


        // dataLen is byte data[0]
    void displayDebugMessage(const char *caller, byte errMscType, const byte *data);
    // void displayMyData(const char *caller, byte errMscType, RXTX_DATA *pData, bool fprintRAW=true);
    void displayMyData(const char *caller, byte errMscType, RXTX_DATA *pData);
    void prova(const char *caller);