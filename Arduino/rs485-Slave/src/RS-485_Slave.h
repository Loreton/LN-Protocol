#if not defined I_AM_MY485
    #define I_AM_MY485

    #define RS485_TX_PIN        2   // D2  DI
    #define RS485_RX_PIN        3   // D3  R0
    #define RS485_ENABLE_PIN    4   // D4  DE/RE up-->DE-->TX  down-->RE-->RX
    #define LED_PIN             13
    #define Addr0             A7
    #define Addr1             A6

#endif