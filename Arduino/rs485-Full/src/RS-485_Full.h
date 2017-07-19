#if not defined I_AM_MY485
    #define I_AM_MY485

    #define RS485_TX_PIN        2   // D2  DI
    #define RS485_RX_PIN        3   // D3  R0
    #define RS485_ENABLE_PIN    4   // D4  DE/RE up-->DE-->TX  down-->RE-->RX
    #define LED_PIN             13



    // #if defined I_AM_MAIN__
    // #ifdef I_AM_MAIN__
        byte        myEEpromAddress;        // who we are
        RXTX_DATA   RxTx, *pData;             // struttura dati

        //.............0 1 234567890123
        char myID[] = "\r\n?[xxx] - "; // i primi due byte saranno CR e LF
                                        // ? E:Echo-Simulate, R:Relay S:Slave
        unsigned long responseDelay = 0;

    // #else
    //     extern byte    myEEpromAddress    ;        // who we are
    //     extern RXTX_DATA   RxTx, *pData;             // struttura dati
    //     extern char myID[]; // i primi due byte saranno CR e LF
    //     extern unsigned long responseDelay;

    // #endif

    enum payLoadMap  {  DATALEN=0,
                        SENDER_ADDR,
                        DESTINATION_ADDR,
                        SEQNO_HIGH,
                        SEQNO_LOW,
                        COMMAND,
                        PAYLOAD,
                    };

    enum rs485_Commands  {  ECHO_CMD=1,
                    };

    // ##########################################
    // # definizione delle seriali
    // ##########################################


    /*
        rename in Serial232 per comodità per la parte Relay
        ma posso continuare ad usare anche solo Serial
    */
    HardwareSerial & Serial232 = Serial;
    SoftwareSerial  Serial485 (RS485_RX_PIN, RS485_TX_PIN);    // receive pin, transmit pin


    // ------ RS485 callback routines
    void WriteSerial485(const byte what)   {       Serial485.write (what); }
    int  AvailableSerial485()              {return Serial485.available (); }
    int  ReadSerial485()                   {return Serial485.read (); }

    // ------ Serial callback routines
    void Write232(const byte what)           {       Serial.write (what); }
    int  Available232()                      {return Serial.available (); }
    int  Read232()                           {return Serial.read (); }



    // ------ funzioni di comodo per chiamare direttamente la seriale desiderata
    inline void sendMsg485(RXTX_DATA *txData, WriteCallback fSend=WriteSerial485 ) {
        sendMsg (txData, fSend);
    }

    inline byte recvMsg485(RXTX_DATA *rxData, ReadCallback fRead=ReadSerial485, AvailableCallback fAvailable=AvailableSerial485) {
        return recvMsg (rxData, fRead, fAvailable);
    }


    // ------ funzioni di comodo per chiamare direttamente la seriale desiderata
    inline void sendMsg232(RXTX_DATA *txData, WriteCallback fSend=Write232) {
        sendMsg (txData, fSend);
    }

    inline byte recvMsg232(RXTX_DATA *rxData, ReadCallback fRead=Read232, AvailableCallback fAvailable=Available232) {
        return recvMsg (rxData, fRead, fAvailable);
    }


#endif