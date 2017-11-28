/*
Author:     Loreto Notarantonio
version:    LnVer_2017-11-12_18.44.34

Scope:      Funzione di slave.
                Prende i dati dalla rs485, verifica l'indirizzo di destinazione e
                se lo riguarda processa il comando ed invia la risposta.
*/

#include <Boards.h>
unsigned char respData[MAX_DATA_SIZE];
int pinNO;

// bool firstRun = true;
// ################################################################
// # - M A I N     Loopslave
// #    - riceviamo i dati da rs485
// #    - elaboriamo il comando ricevuto
// #    - rispondiamo se siamo interessati
// lo slave scrive sulla seriale come debug
// ################################################################
void Slave_Main() {
    if (firstRun) {
        pData->fDisplayMyData       = true;                // display dati relativi al mio indirizzo
        pData->fDisplayOtherHeader  = true;                // display dati relativi ad  altri indirizzi
        pData->fDisplayOtherFull    = false;                // display dati relativi ad  altri indirizzi
        pData->fDisplayRawData      = false;                // display raw data

        pData->timeout          = 5000;
    }

    // Serial.println();
    byte rcvdRCode = recvMsg485(pData);
    // byte rcvdRCode = 0;

    if (rcvdRCode == LN_OK) {
        processRequest(pData);
    }

    else if (pData->rx[fld_DATALEN] == 0) {
        Serial.print(myID);
        Serial.print(F("rcvdRCode: "));Serial.print(rcvdRCode);
        Serial.print(F(" - Nessuna richiesta ricevuta in un tempo di mS: "));Serial.print(pData->timeout);
        Serial.println();

    }

    else { // DEBUG
        Serial.print(myID);
        Serial.print(F("rcvdRCode: "));Serial.print(rcvdRCode);
        Serial.println(F(" - errore non identificato: "));
    }

}



// #############################################################
// #
// #############################################################
void processRequest(RXTX_DATA *pData) {
    byte senderAddr = pData->rx[fld_SENDER_ADDR];
    byte destAddr   = pData->rx[fld_DESTINATION_ADDR];
    // byte fld_subCommand = pData->rx[fld_SUBCOMMAND];
    byte analogValue = 0;
    byte pinNO        = pData->tx[fld_COMMAND_DATA+1];
    byte valueToWrite = pData->tx[fld_COMMAND_DATA+2];



    byte readValue  = 0;
    // byte writeValue = 0;
    // byte rCode      = 0;
    char returnDATA[20];

    if (destAddr != myEEpromAddress) {    // non sono io.... commento sulla seriale
        // [Slave-012] - RX-data [rcvdCode: OK] - [00/000] --> [0B/011] - SeqNO: 00007 - [it's NOT for me...]

        return;
    }

    char pollingAnswer[] = "Polling answer!";
    char unknownCommand[] = "UNKNOWN command";
    char AnalogCMD[]  = "ANALOG";
    char DigitalCMD[] = "DIGITAL";
    char readingPin[] = " - reading pin: ";
    char writingPin[] = " - writing pin: ";
    // byte myANALOG_PINS[] =  {PIN_A0, PIN_A1, PIN_A2, PIN_A3, PIN_A4, PIN_A5, PIN_A6, PIN_A7 };

    // copiamo RX to TX per poi andare a modificare solo il necessario
    copyRxMessageToTx(pData);

    Serial.println(F(""));
    Serial.print(F(" DIGITAL command     -> "));Serial.println(DIGITAL_CMD);
    Serial.print(F(" ANALOG  command     -> "));Serial.println(ANALOG_CMD);
    Serial.print(F(" Command    ricevuto -> "));Serial.print(pData->rx[fld_COMMAND]);Serial.print(F("."));Serial.println(pData->rx[fld_SUBCOMMAND]);
    switch (pData->rx[fld_COMMAND]) {

            // ------------------------------------------------------
            //                  ANALOG
            // pin:     the pin to write to. Allowed data types: int.
            // value:   the duty cycle: between 0 (always off) and 255 (always on). Allowed data types: int
            // Es.:
            //      val = analogRead(analogPin);   // read the input pin
            //      analogWrite(ledPin, val / 4);  // analogRead values go from 0 to 1023, analogWrite values from 0 to 255
            // ------------------------------------------------------
        case ANALOG_CMD:
            Serial.print("\n\n");Serial.print(TAB);Serial.print(AnalogCMD);
            Serial.print(" is pin Analog? ->");Serial.print(IS_PIN_ANALOG(pinNO)); // board.h
            // for(i=5; i < 11; i++);
            switch (pData->rx[fld_SUBCOMMAND]) {

                case READ_PIN:
                    Serial.print(readingPin);Serial.println(pinNO);
                    analogValue = LnReadAnalogPin(pinNO);
                    break;

                case WRITE_PIN:
                    Serial.print(writingPin);Serial.println(pinNO);
                    analogWrite(pinNO, valueToWrite);
                    delay(500);
                    analogValue = LnReadAnalogPin(pinNO); // re-read to check the value and return it
                    break;
            }
            returnDATA[0] = (char) analogValue;
            setCommandData(pData->tx, returnDATA, 1);
            pData->tx[fld_CMD_RCODE] = OK;

            // ------------------------------------------------------
            //                  DIGITA
            // pin:     the pin to write to. Allowed data types: int.
            // value:   the duty cycle: between 0 (always off) and 255 (always on). Allowed data types: int
            // Es.:
            //      val = analogRead(analogPin);   // read the input pin
            //      analogWrite(ledPin, val / 4);  // analogRead values go from 0 to 1023, analogWrite values from 0 to 255
            // ------------------------------------------------------
        case DIGITAL_CMD:
            Serial.print("\n\n");Serial.print(TAB);Serial.print(DigitalCMD);Serial.print(readingPin);
            Serial.print(": ");Serial.print(pinNO);Serial.print(" - is pin Digital?: ");Serial.print(IS_PIN_DIGITAL(pinNO)); // board.h
            switch (pData->rx[fld_SUBCOMMAND]) {

                case READ_PIN:
                    Serial.print(readingPin);Serial.println(pinNO);
                    readValue = digitalRead(pinNO);
                    setCommandData(pData->tx, pollingAnswer, sizeof(pollingAnswer));
                    break;

                case WRITE_PIN:
                    Serial.print(writingPin);Serial.println(pinNO);
                    digitalWrite(pinNO, valueToWrite);
                    delay(500);
                    readValue = digitalRead(pinNO);
                    break;
            }
            returnDATA[0] = (char) readValue;
            setCommandData(pData->tx, returnDATA, 1);
            pData->tx[fld_CMD_RCODE] = OK;

        case PWM_CMD:
            switch (pData->rx[fld_SUBCOMMAND]) {
                case READ_PIN:
                break;

                case WRITE_PIN:
                break;
            }

        case SLAVE_POLLING_CMD:
            switch (pData->rx[fld_SUBCOMMAND]) {
                case REPLY:
                    Serial.print("\n\n");Serial.print(TAB);Serial.println(F("preparing response message... "));

                    setCommandData(pData->tx, pollingAnswer, sizeof(pollingAnswer));
                    pData->tx[fld_CMD_RCODE] = OK;
                }
                break;

        case SET_PINMODE_CMD:
            // writeEEprom(pData->rx[fld_SUBCOMMAND], pData->rx[fld_COMMAND_DATA]);
            // pData->tx[fld_CMD_RCODE] = OK;
            break;

        default:
            setCommandData(pData->tx, unknownCommand    , sizeof(unknownCommand ));
            pData->tx[fld_CMD_RCODE] = UNKNOWN_CMD;
            break;
    }

    pData->tx[fld_DESTINATION_ADDR] = senderAddr;
    pData->tx[fld_SENDER_ADDR]      = myEEpromAddress;
    sendMsg485(pData);
}



int readPWM(int pin) {
    return 0;
}

int writePWM(int pin) {
    return 0;
}



// ##################################################
// # LnReadAnalogPin(int pin)
// ##################################################
byte LnWriteAnalogPin(int pin) {
    return 0;
}
// ##################################################
// # LnReadAnalogPin(int pin)
// ##################################################
int LnReadAnalogPin(int pin) {
const int MAX_READS = 10;
int readings[MAX_READS];           // the readings from the analog input
int readInx = 0;              // the index of the current reading
int totValue = 0;                  // the running totValue
int avgValue = 0;                // the avgValue

        // Lettura del pin
    for (readInx = 0; readInx < MAX_READS; readInx++) {
        readings[readInx] = analogRead(pin);    // lettura pin

        // add the reading to the totValue:
        totValue = totValue + readings[readInx];
        delay(100);        // delay in between reads for stability
    }

    // calculate the avgValue:
    avgValue = totValue / MAX_READS;

        // DEBUG Display valori
    boolean fDEBUG = false;
    if (fDEBUG) {
        Serial.print("[PIN ");Serial.print(pin, HEX);Serial.print("] - ");
        for (readInx = 0; readInx < MAX_READS; readInx++) {
            Serial.print(" ");Serial.print(readings[readInx], DEC);
        }
        Serial.print(" avgValue = ");Serial.print(avgValue, DEC);
        float Voltage = avgValue * (5.0 / 1023.0);
        Serial.print(" Voltage = ");Serial.println(Voltage, 2);
        Serial.println();
    }

    return avgValue;
}


#if 0
// #############################################################
// # Arduino nano ha EEPROM = 1KBytes
// # salviamo il pinMode dei pin nella EEPROM
// # 0x10 per digital-pin > 0x80 se INPUT
// # 0x20 per analog-pin    non importa input/output
// # 0x30 per pwm-pin     > 0x80 se INPUT
// # pinType = enum fld_rs485_SubCOMMANDs in LnRs485.h
// #############################################################
void writeEEprom(byte pinType,  RXTX_DATA *pData) {
byte startAddress = 0;
byte fld_subCommand = pData->rx[fld_SUBCOMMAND];

    if      (fld_subCommand == DIGITAL_OUT)  startAddress = 0x10;
    else if (fld_subCommand == DIGITAL_INP)  startAddress = 0x20;
    else if (fld_subCommand == ANALOG_INP)   startAddress = 0x30;
    else if (fld_subCommand == ANALOG_OUT)   startAddress = 0x40;
    else if (fld_subCommand == PWM_OUT)      startAddress = 0x50;
    else if (fld_subCommand == PWM_INP)      startAddress = 0x60;
    else                                 startAddress = 0x0;

    // copiamo il codice errore nei [....]
    for (byte i=7; pinType != 0; i++)
        errorMsg[i] = *pData++;


    if (EEPROM.read (address) != myAddress)
        // EEPROM.write (0, myAddress);
}

#endif