/*
Author:     Loreto Notarantonio
version:    LnVer_2017-11-12_18.44.34

Scope:      Funzione di slave.
                Prende i dati dalla rs485, verifica l'indirizzo di destinazione e
                se lo riguarda processa il comando ed invia la risposta.
*/

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

    else if (pData->rx[DATALEN] == 0) {
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
    byte senderAddr = pData->rx[SENDER_ADDR];
    byte destAddr   = pData->rx[DESTINATION_ADDR];
    byte readValue = 0;

    if (destAddr != myEEpromAddress) {    // non sono io.... commento sulla seriale
        // [Slave-012] - RX-data [rcvdCode: OK] - [00/000] --> [0B/011] - SeqNO: 00007 - [it's NOT for me...]

        return;
    }

//@todo: inserire l'indirizzo nel comando myMsg...
    char myMsg1[] = "Polling answer!";
    char myMsg2[] = "devo scrivere il pin";
    char myMsg3[] = "Comando non riconosciuto";

    copyRxMessageToTx(pData);
    switch (pData->rx[COMMAND]) {

        case SLAVE_POLLING:
            if (pData->rx[SUBCOMMAND] == REPLY) {
                Serial.print("\n\n");Serial.print(TAB);Serial.println(F("preparing response message... "));

                setCommandData(pData->tx, myMsg1, sizeof(myMsg1));
                pData->tx[CMD_RCODE] = OK;
            }
            break;

        case READ_PIN:
            pinNO = pData->tx[COMMAND_DATA+1];
            Serial.print("\n\n");Serial.print(TAB);Serial.print(F("lettura del pin: "));Serial.println(pinNO);

            if (pData->rx[SUBCOMMAND] == ANALOG) {
                readValue = LnReadAnalogPin(pinNO);
            }

            else if (pData->rx[SUBCOMMAND] == DIGITAL) {
                readValue = digitalRead(pinNO);
            }

            else if (pData->rx[SUBCOMMAND] == PWM) {
                readValue = readPWM(pinNO);
            }

            else {
                readValue = 0;
            }

            respData[0] = readValue;
            // setCommandData(pData->tx, respData, 1);
            pData->tx[CMD_RCODE] = OK;
            break;

        case WRITE_PIN:
            setCommandData(pData->tx, myMsg2, sizeof(myMsg2));
            pData->tx[CMD_RCODE] = OK;
            break;

        case SET_PINMODE:
            // writeEEprom(pData->rx[SUBCOMMAND], pData->rx[COMMAND_DATA]);
            // pData->tx[CMD_RCODE] = OK;
            break;

        default:
            setCommandData(pData->tx, myMsg3, sizeof(myMsg3));
            pData->tx[CMD_RCODE] = UNKNOWN_CMD;
            break;
    }

    pData->tx[DESTINATION_ADDR] = senderAddr;
    pData->tx[SENDER_ADDR]      = myEEpromAddress;
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
// # pinType = enum rs485_SubCOMMANDs in LnRs485.h
// #############################################################
void writeEEprom(byte pinType,  RXTX_DATA *pData) {
byte startAddress = 0;
byte subCommand = pData->rx[SUBCOMMAND];

    if      (subCommand == DIGITAL_OUT)  startAddress = 0x10;
    else if (subCommand == DIGITAL_INP)  startAddress = 0x20;
    else if (subCommand == ANALOG_INP)   startAddress = 0x30;
    else if (subCommand == ANALOG_OUT)   startAddress = 0x40;
    else if (subCommand == PWM_OUT)      startAddress = 0x50;
    else if (subCommand == PWM_INP)      startAddress = 0x60;
    else                                 startAddress = 0x0;

    // copiamo il codice errore nei [....]
    for (byte i=7; pinType != 0; i++)
        errorMsg[i] = *pData++;


    if (EEPROM.read (address) != myAddress)
        // EEPROM.write (0, myAddress);
}

#endif