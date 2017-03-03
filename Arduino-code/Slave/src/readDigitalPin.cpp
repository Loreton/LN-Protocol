#include "LnProtocolSlave.h"

byte        counter           = 0;   // contatore per messaggi inviati

//#####################################################
// #  readDigitalPin()
// #  REQ: STX ! MasterAddress  ! slaveAddress    !  readPin    ! numeroPIN
// #  RSP: STX ! slaveAddress   ! masterAddress   !  readPin    ! numeroPIN, value
// #
//#####################################################
void readDigitalPin(byte slaveAddress, byte pinNO) {
    byte TxMsg[MAX_BufferSize];
    byte i;

    byte dataLen = 0;
    TxMsg [dataLen++] = ++counter;   // DEBUG - Andrà tolto nella versione definitiva.
    TxMsg [dataLen++] = STX;
    TxMsg [dataLen++] = MASTER_ADDRESS;
    TxMsg [dataLen++] = slaveAddress;
    TxMsg [dataLen++] = READ_PIN_CMD;
    TxMsg [dataLen++] = pinNO;
    byte CRC8value    = LnCRC8(&TxMsg[1], dataLen); // skip del STXed ETX
    TxMsg [dataLen++] = CRC8value;
    TxMsg [dataLen++] = ETX;

        // Turn on the LED on pin LED to indicate that we are about to transmit data
    digitalWrite(LED, HIGH);

    // vw_send((byte *)TxMsg, &dataLen);
    vw_send(TxMsg, dataLen);

        // Wait until the data has been sent
    vw_wait_tx();

        // Turn off the LED on pin LED to indicate that we have now sent the data
    digitalWrite(LED, LOW);

    // --------------------------
    // - DEBUG - PRINT MESSAGE
    // --------------------------
    #if 0
    #endif

    Serial.print("SENT: "); printHex(TxMsg, dataLen, "\r\n");
}
