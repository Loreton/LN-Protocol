/*
Author:     Loreto Notarantonio
version:    LnVer_2017-11-30_19.06.45

Scope:      Funzione di relay.
                Prende i dati provenienti da una seriale collegata a RaspBerry
                ed inoltra il comando sul bus RS485.
                Provvede ovviamente a catturare la risposta e reinoltrarla a RaspBerry.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/


#define RETURN_RS485_TO_MASTER   // on MASTER-RELAY-RS232 port return RS485 data or Text data
#ifdef MASTER_SIMULATOR

// ##########################################################
// se vogliamo che Arduino invii un echo autonomamente
// ##########################################################
void loop_MasterSimulator() {
    unsigned long RX_TIMEOUT = 2000;
    // forziamo myAddress a MASTER
    // myEEpromAddress = 0;

    #ifdef RETURN_RS485_TO_MASTER
        returnRs485ToMaster         = true;
        pData->fDisplayMyData       = false;                // display dati relativi al mio indirizzo
        pData->fDisplayOtherHeader  = false;                // display dati relativi ad  altri indirizzi
        pData->fDisplayOtherFull    = false;                // display dati relativi ad  altri indirizzi
        pData->fDisplayRawData      = false;                // display raw data

        Simulator(pData);

        // proviamo ad intercettare una richiesta da RaspBerry per massimo
        Relay_Main(RX_TIMEOUT);

    #else
        returnRs485ToMaster         = false;
        pData->fDisplayMyData       = true;                // display dati relativi al mio indirizzo
        pData->fDisplayOtherHeader  = true;                // display dati relativi ad  altri indirizzi
        pData->fDisplayOtherFull    = true;                // display dati relativi ad  altri indirizzi
        pData->fDisplayRawData      = false;                // display raw data
        Serial.print(myID);Serial.println(F("Sono in Relay simulation mode"));

        Simulator(pData);
        Serial.println();
    #endif


    delay(5000);
}

// #############################################################
// # Prepariamo un pacchetto di sumulazione
// #    come se fosse invocato da Master (addr=0)
// #    ...facciamo il forwarding sulla rs485
// #    ...attendiamo la risposta
// #    ...inviamo il pacchetto verso Master.
// #############################################################
void Simulator(RXTX_DATA *pData) {
    static int seqNO   = 0;
    volatile byte i;
    byte dataLen;

    int destAddresses[] = {11, 12, 13};
    // int destAddresses[] = {12};
    // int destAddresses[] = {11};
    byte nElem = sizeof(destAddresses)/sizeof(int);

    #define POLLING         1
    #define DIGITALREAD     2
    #define DIGITALWRITE    3
    #define TOGGLEPIN       4
    #define SIMULATION_TYPE TOGGLEPIN


    for (i=0; i<nElem; i++) {
        dataLen = 0;

            // ---------------------------------------------------------
            // - dovendo simulare la ricezione da parte del raspberry
            // - preparo un messaggio come se fosse stato ricevuto
            // ---------------------------------------------------------
        pData->rx[fld_SENDER_ADDR]      = MASTER_ADDRESS;                                    // proviene dal master
        pData->rx[fld_DESTINATION_ADDR] = destAddresses[i];                    // DA
        pData->rx[fld_SEQNO_HIGH]       = seqNO >> 8;
        pData->rx[fld_SEQNO_LOW]        = seqNO & 0x00FF;
        pData->rx[fld_CMD_RCODE]        = LN_OK;

        #if SIMULATION_TYPE==POLLING
            char dataCmd[]  = "Simulation request!";
            pData->rx[fld_COMMAND]          = POLLING_CMD;
            pData->rx[fld_SUBCOMMAND]       = REPLY;
            dataLen = sizeof(dataCmd);
        #elif SIMULATION_TYPE==DIGITALREAD
            char data[]  = "......";
            pData->rx[fld_COMMAND]         = DIGITAL_CMD;
            pData->rx[fld_SUBCOMMAND]      = READ_PIN;
            data[dataLen++]  = D01;     // pin number
        #elif SIMULATION_TYPE==DIGITALWRITE
            char data[]  = "......";
            pData->rx[fld_COMMAND]         = DIGITAL_CMD;
            pData->rx[fld_SUBCOMMAND]      = WRITE_PIN;
            data[dataLen++]  = D13;     // pin number
            data[dataLen++]  = LOW;     // value
        #elif SIMULATION_TYPE==TOGGLEPIN
            char data[]  = "......";
            pData->rx[fld_COMMAND]         = DIGITAL_CMD;
            pData->rx[fld_SUBCOMMAND]      = TOGGLE_PIN;

            if (destAddresses[i] == 11)
                data[dataLen++]  = D11;     // pin number
            else if (destAddresses[i] == 12)
                data[dataLen++]  = D13;     // pin number
            else
                data[dataLen++]  = D13;     // pin number

        #endif

        // pData->rx[fld_DATALEN]          = fld_SUBCOMMAND;



            // come comandData inviamo un testo di esempio
        setDataCommand(pData->rx, data, dataLen);

        // - simuliamo la ricezione con rCode=LN_OK
        byte rCode = LN_OK;
        if (rCode == LN_OK) {
            Relay_fwdToRs485(pData);
                // qualsiasi esito il msg è pronto da inviare sulla rs232
            byte rcvdRCode = Relay_waitRs485Response(pData, 2000);
            Relay_fwdToRaspBerry(pData, rcvdRCode, returnRs485ToMaster);
        }


        delay(500); // aspettiamo tra uno slave ed il successivo
    }
    seqNO++;

}
#endif