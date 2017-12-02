#if not defined I_AM_MY485
    #define I_AM_MY485

    #define RS485_TX_PIN        D02   // D2  DI
    #define RS485_RX_PIN        D03   // D3  R0
    #define RS485_ENABLE_PIN    D04   // D4  DE/RE up-->DE-->TX  down-->RE-->RX


    #define MASTER_ADDRESS      0

    #define MASTER_SIMULATOR
    #define RETURN_TEXT_DATA_TO_MASTER   // on MASTER-RELAY-RS232 port return RS485 data or Text data


    RXTX_DATA   RxTx, *pData;             // struttura dati


    #if defined (I_AM_MAIN_)
        byte  myEEpromAddress = 0;        // who we are
        char sharedWorkingBuff[50];
        bool firstRun = true;
        const char TAB4[] = "\n    ";

    #else
        extern byte  myEEpromAddress;        // who we are
    #endif

    // #define RELAY_ECHO    = 1;
    // #define SLAVE_ECHO    = 2;
    // #define SLAVE_POLLING = 3;
    // #define READ_PIN      = 4;
    // #define WRITE_PIN     = 5;
    // #define SET_PINMODE   = 6;


    enum rs485_COMMANDs {
                            RELAY_ECHO_CMD          = 0x01,
                            SLAVE_ECHO_CMD          = 0x02,
                            POLLING_CMD             = 0x03,
                            SET_PINMODE_CMD         = 0x21,
                            DIGITAL_CMD             = 0x31,
                            ANALOG_CMD              = 0x32,
                            PWM_CMD                 = 0x33,
                        };

    enum rs485_SubCOMMANDs {
                            NO_REPLY                = 0x01,     // for echo command
                            REPLY                   = 0x02,     // for echo command
                            READ_PIN                = 0x04,     // for analog/digital commands
                            WRITE_PIN               = 0x05,     // for analog/digital commands
                            TOGGLE_PIN              = 0x06,     // for digital commands
                        };


    enum rs485_ERRORs {
                            OK            = 0x00,    // ERRORE nel ricevere dati da rs485
                            RS485_ERROR   = 0x01,    // ERRORE nel ricevere dati da rs485
                            TIMEOUT_ERROR = 0x02,    // TIMEOUT nel ricevere dati da rs485
                            UNKNOWN_CMD   = 0x03,    // TIMEOUT nel ricevere dati da rs485
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