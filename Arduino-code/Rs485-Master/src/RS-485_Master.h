#if not defined I_AM_MY485
    #define I_AM_MY485

    // const byte ENABLE_PIN   =  4;
    #define RS485_TX_PIN        2   // D2
    #define RS485_RX_PIN        3   // D3
    #define RS485_ENABLE_PIN    4   // D4
    #define LED_PIN             13


    // const byte myADDR       = 1;
    // const char *devName     = "[Slave01]";
    // int nLoops              = 0;

    // unsigned long timeOUT   = 10000;

    // --------------------
    //     mi serve per verificare i dati e l'ordine con cui sono
    //     stati inviati inclusi STX, CRC, ETX
    //     DEBUG_sentMsg[0] contiene lunghezza dei dati
    // --------------------
    // byte DEBUG_TxRxMsg [200] = "                                                                ";   // gli faccio scrivere il messaggio inviato con relativo CRC

#endif