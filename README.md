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
        DATALEN                   - lunghezza dei dati escluso STX ed ETX
        SENDER_ADDR               - Dest Address      (FF = Broadcast)
        DESTINATION_ADDR          - source Address    (00 = Master)
        SEQNO_HIGH                - numero del messaggio utile per associare la risposta
        SEQNO_LOW                 -
        COMMAND                   - comando da eseguire
        RCODE                     - esito del comando
        USER_DATA                 - dati necessari per l'esecuzione del comando oppure i dati di risposta
        ....                      -
    CRC                           - CRC
    ETX                           - ETX

    Commands Sample                                                         - Commnad
        ; 01 xx                                                             - readPin       - pinNumber
        ; 02 xx                                                             - readRelè      - releNumber
        ; 03 xx                                                             - readLED       - ledNumber
        ; 04 I2C_address cmd byte0, byte1, ...., bytex                      - readI2C
        ; -- --                                                             -
        ; 81 xx ON|OFF                                                      - writePin      - pinNumber
        ; 82 xx ON|OFF                                                      - writeRelè     - releNumber
        ; 83 xx ON|OFF                                                      - writeLED      - ledNumber
        ; 84 I2C_address cmd byte0, byte1, ...., bytex                      - writeI2C



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