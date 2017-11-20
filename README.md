# LN-Protocol
Tentativo di implementazione un protocollo di comunicazione per la gestione ed il controllo di diversi dispositivi tramite RaspBerry-->Arduino.

Il protocollo si basa su RS-485 oppure Wireless.

Non è previsto che lo Slave prenda iniziativa della trasmissione.

Tutto il controllo è demandato al MASTER (RaspBerr) il quale tramite un protocollo di polling provvede ad interrogare tutti gli SLAVE predefiniti. Questo permette di evitare conflitti nelle comunicazioni.

Tutto il processo parte dal RaspBerry il quale conosce tutti i dispositivi e per ognuno di essi l'opportuno comando da inviare per raccogliere le informazioni.
Nel caso di RS-485 RaspBerry è autonomo nell'inviare il comando e raccogliere le info.
Nel caso di Wireless RaspBerry si deve appoggiare ad un Arduino locale che provvede ad eseguire il comando per lui. Il dialogo tra RaspBerry ed ArduinoLocale avviene anmcora tramite RS-485.


Sintassi generica dei comandi string Master to Slave:

    STX                           - STX
        DATALEN                   - datalen out of STX ed ETX
        SENDER_ADDR               - Dest   Address
        DESTINATION_ADDR          - Source Address    (00 = Master)
        SEQNO_HIGH                - Sequence message number (To associate Req/Resp)
        SEQNO_LOW                 -
        CMD_RCODE                 - Execution of Command returnCode (ignored during TX)
        COMMAND                   - Command to be executed
        SUBCOMMAND                - SubCommand... related to Command
        COMMAND_DATA              - TX-data to be used during command execution RX-response data
        ....                      -
    CRC                           - CRC
    ETX                           - ETX

    Commands Sample                                                         - Commnad
        - RELAY_ECHO                                                        -
            NO_REPLY
            REPLY
        ;
        - SLAVE_ECHO                                                        -
            NO_REPLY
            REPLY

        - SLAVE_POLLING                                                     -
        ;
        - READ_PIN                                                          -
            DIGITAL pinNO
            ANALOG  pinNO
            PWM     pinNO
        ;
        - WRITE_PIN                                                         -
            DIGITAL pinNO
            ANALOG  pinNO
            PWM     pinNO
        ;
        - SET_PINMODE                                                       -
            will be soon available...
        ;
        - I2C                                                       -
            I2C_address cmd byte0, byte1, ...., bytex


------------------------!-----------------! -------------!----------------------------------------------------------------
           origin       !    destination  !   CMD        ! parameters
------------------------!-----------------! -------------!----------------------------------------------------------------
    CMD: MasterAddress  ! slaveAddress    !  ReadI2C     ! I2C_address cmd byte0, byte1, ...., bytex
    RSP:                !                 !  ReadI2C     ! STATUS_BYTE - dati....
                        !                 !              !
    CMD: MasterAddress  ! slaveAddress    !  WriteI2C    ! I2C_address cmd byte0, byte1, ...., bytex
    RSP:                !                 !  WriteI2C    ! STATUS_BYTE - dati....
                        !                 !              !
    CMD: MasterAddress  ! slaveAddress    !  ReadPin     ! numeroPIN
    RSP:                !                 !  ReadPin     ! numeroPIN
                        !                 !              !
    CMD: MasterAddress  ! slaveAddress    !  WritePin    ! numeroPIN, value
    RSP:                !                 !  WritePin    ! numeroPIN



TAG v01.07:
    Arduino-Relay partito in SIMULATE_ECHO. Invia il messaggio di echo sulla rs485. Con una pen_usb_rs485 collegata al RaspBerry si può monitorare il bus con il comando:
    python3.4 /home/pi/GIT-REPO/LnProtocol/RaspBerry/__main__.py monitor rs485 --port ttyUSBxxx (pen_usb_rs485)