// ########################################
// Author:  Loreto notarantonio
// Version: LnVer_2017-11-29_19.04.39
// ########################################

#if defined(ARDUINO) && ARDUINO >= 100
    #include "Arduino.h"
#else
    #include "WConstants.h"
#endif

#define RECV_DEFAULT_TIMEOUT 2*1000

// #if not defined I_AM_RS485_PROTOCOL_H
#if defined I_AM_RS485_PROTOCOL_CPP
    // #define I_AM_RS485_PROTOCOL_H
                            //-- 01234567
    const char *errMsg[]    = { "OK",
                                "OVERFLOW",
                                "BAD-CRC",
                                "BAD-CHAR",
                                "TIMEOUT",
                                "PAYLOAD",
                                "DEBUG",
                            };



    // extern byte myEEpromAddress;


#else
    // extern const char TAB[];
    extern const char *errMsg[];

#endif



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

        #define MAX_DATA_SIZE     60
    // definizione messa qui per comodità con  il printMessage.
    enum RXTX_MAP  {
                        fld_DATALEN=0,          // - lunghezza dei dati escluso STX ed ETX
                        fld_SENDER_ADDR,        // - Dest Address      (FF = Broadcast)
                        fld_DESTINATION_ADDR,   // - source Address    (00 = Master)
                        fld_SEQNO_HIGH,         // - numero del messaggio utile per associare la risposta
                        fld_SEQNO_LOW,          // -
                        fld_CMD_RCODE,          // - rCode di ritorno per il comando eseguito (in TX è ignorato)
                        fld_COMMAND,            // - comando da eseguire
                        fld_SUBCOMMAND,         // - eventuale dettaglio per il comando
                        fld_DATA_COMMAND,      // - TX - dati necessari al comando per la sua corretta esecuzione/RX - dati di risposta
                    };

//  identifica il byte che contiene la lunghezza dati
    #define pDATALEN     0
    // byte pDATALEN=0;


    // the data we broadcast to each other device
    typedef struct  {

        unsigned char   rx[MAX_DATA_SIZE];        // byte[0] is dataLen
        unsigned char   tx[MAX_DATA_SIZE];        // byte[0] is dataLen
        unsigned char   raw[MAX_DATA_SIZE*2+2];   // byte[0] is dataLen SIZE = dataLen + STX+ETX
        byte            Tx_CRCcalc;    // CRC value
        byte            Rx_CRCcalc;    // CRC value
        byte            Rx_CRCrcvd;    // CRC value

        bool            fDisplayMyData      = false;       // display dati relativi al mio indirizzo
        bool            fDisplayOtherHeader = false;       // display solo header di altri indirizzi
        bool            fDisplayOtherFull   = false;       // display dati di altri indirizzi (include l'header)
        bool            fDisplayRawData     = false;       // per fare il print del rawData

        byte            myEEpromAddress;                // indirizzo identificativo di Arduino
        char            *myID;                          // stringa identificativo di Arduino
        unsigned long   timeout         = RECV_DEFAULT_TIMEOUT;        // receive timeout

    }  RXTX_DATA, *pRXTX_DATA;

    typedef void (*WriteCallback)  (const byte what);   // send a byte to serial port
    typedef int  (*AvailableCallback)  ();              // return number of bytes available
    typedef int  (*ReadCallback)  ();                   // read a byte from serial port



    void sendMsg (RXTX_DATA *rxData, WriteCallback fSend);
    byte recvMsg (RXTX_DATA *rxData, ReadCallback fRead, AvailableCallback fAvailable);


        // dataLen is byte data[0]
    void displayDebugMessage(const char *caller, byte errMscType, const byte *data);
    void displayMyData(const char *caller, byte errMscType, RXTX_DATA *pData);
    void prova(const char *caller);



    void copyRxMessageToTx(RXTX_DATA *pData);
    void setDataCommand(byte *pData, char cmdData[], byte dataLen);
    byte waitRs485Response(RXTX_DATA *pData, unsigned long TIMEOUT);

