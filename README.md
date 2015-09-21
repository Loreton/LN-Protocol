# LN-Protocol
Tentativo di implementazione un protocollo di comunicazione
per permettere la gestione ed il controllo di diversi dispositivi
RaspBerry o Arduino.

Il protocollo si dovrebbe appoggiare al RS-485 oppure Wireless.
Il protocollo non prevede che lo Slave inizi una trasmissione.
Tutto il controllo è demandato al MASTER il quale tramite un
protocollo di polling provvede ad interrogare tutti gli SLAVE predefiniti.
Anche se un pò più oneroso, questo permette di evitare conflitti nelle comunicazioni.


Sintassi generica dei comandi string Master to Slave:

    02                                                                          - STX
    XX                                                                          - Slave Address
        Command                                                                 - Commnad
            ; 01 xx                                                             - readPin       - pinNumber
            ; 02 xx                                                             - readRelè      - releNumber
            ; 03 xx                                                             - readLED       - ledNumber
            ; 04 I2C_address cmd byte0, byte1, ...., bytex                      - readI2C
            ; -- --                                                             -
            ; 81 xx ON|OFF                                                      - writePin      - pinNumber
            ; 82 xx ON|OFF                                                      - writeRelè     - releNumber
            ; 83 xx ON|OFF                                                      - writeLED      - ledNumber
            ; 84 I2C_address cmd byte0, byte1, ...., bytex                      - writeI2C
    YY                                                                          - CRC
    03                                                                          - ETX



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

