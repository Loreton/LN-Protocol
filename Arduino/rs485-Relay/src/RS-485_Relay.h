#if not defined I_AM_MY485
    #define I_AM_MY485

    #define RS485_TX_PIN        2   // D2  DI
    #define RS485_RX_PIN        3   // D3  R0
    #define RS485_ENABLE_PIN    4   // D4  DE/RE up-->DE-->TX  down-->RE-->RX
    #define LED_PIN             13


    enum payLoadMap  {  DATALEN=0,
                        SENDER_ADDR,
                        DESTINATION_ADDR,
                        SEQNO_HIGH,
                        SEQNO_LOW,
                        PAYLOAD,
                        COMMAND=PAYLOAD,
                    };

    enum rs485_Commands  {  ECHO_CMD=1,
                    };

    // definizione delle seriali
    HardwareSerial & serialPi = Serial; // rename della Serial per comodità
    SoftwareSerial  arduino485 (RS485_RX_PIN, RS485_TX_PIN);  // receive pin, transmit pin


    // ------ RS485 callback routines
    void funcWriteArduino485(const byte what)   {       arduino485.write (what); }
    int  funcAvailableArduino485()              {return arduino485.available (); }
    int  funcReadArduino485()                   {return arduino485.read (); }

    // ------ RS485 callback routines
    void funcWritePi(const byte what)   {       serialPi.write (what); }
    int  funcAvailablePi()              {return serialPi.available (); }
    int  funcReadPi()                   {return serialPi.read (); }



    // ------ funzioni di comodo per chiamare direttamente la seriale desiderata
    inline void sendMsgArduino(RXTX_DATA *rxData, WriteCallback fSend=funcWriteArduino485 ) {
        sendMsg (rxData, fSend);
    }

    inline byte recvMsgArduino(RXTX_DATA *rxData, ReadCallback fRead=funcReadArduino485, AvailableCallback fAvailable=funcAvailableArduino485) {
        return recvMsg (rxData, fRead, fAvailable);
    }


    inline void sendMsgPi(RXTX_DATA *rxData, WriteCallback fSend=funcWritePi) {
        sendMsg (rxData, fSend);
    }

    inline byte recvMsgPi(RXTX_DATA *rxData, ReadCallback fRead=funcReadPi, AvailableCallback fAvailable=funcAvailablePi) {
        return recvMsg (rxData, fRead, fAvailable);
    }


#endif