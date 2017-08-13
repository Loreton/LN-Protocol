#if not defined I_AM_MY485
    #define I_AM_MY485

    #define RS485_TX_PIN        2   // D2  DI
    #define RS485_RX_PIN        3   // D3  R0
    #define RS485_ENABLE_PIN    4   // D4  DE/RE up-->DE-->TX  down-->RE-->RX
    #define LED_PIN             13

    #define MASTER_ADDRESS      0


    RXTX_DATA   RxTx, *pData;             // struttura dati


#if defined (I_AM_MAIN_)
    byte  myEEpromAddress = 0;        // who we are
    char sharedWorkingBuff[50];
    bool firstRun = true;
    const char TAB[] = "\n    ";

#else
    extern byte  myEEpromAddress;        // who we are
#endif


    enum rs485_COMMANDs {
                            ECHO_CMD        = 1,
                            POLLING_CMD     = 2,
                            READPIN_CMD     = 21,
                            WRITEPIN_CMD    = 22,
                        };

    enum rs485_SubCOMMANDs {
                            NO_REPLY       = 0,
                            REPLY          = 1,
                        };


    enum rs485_ERRORs {
                            OK            = 0,    // ERRORE nel ricevere dati da rs485
                            RS485_ERROR   = 1,    // ERRORE nel ricevere dati da rs485
                            TIMEOUT_ERROR = 2,    // TIMEOUT nel ricevere dati da rs485
                            UNKNOWN_CMD   = 3,    // TIMEOUT nel ricevere dati da rs485
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
        digitalWrite(RS485_ENABLE_PIN, ENA_485_TX);               // enable Rs485 sending
        sendMsg (txData, fSend);
        digitalWrite(RS485_ENABLE_PIN, ENA_485_RX);               // set in receive mode
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