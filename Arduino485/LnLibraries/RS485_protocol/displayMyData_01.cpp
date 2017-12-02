
#include "LnFunctions.h"
#include "LnRS485_protocol.h"


// #############################################################
// # const char* text : per ricevere una stringa constante es: "Loreto"
// #############################################################
void displayMyData(const char *caller, byte rCode, RXTX_DATA *pData) {
    const byte *data;
    const byte *raw;
    // byte fPrintData = false;
    byte  rawIndex=0;
    const char TAB4[] = "\n    ";


    byte fDisplayFullData = false;
    byte fDisplayHeader   = (pData->fDisplayMyData + pData->fDisplayOtherHeader + pData->fDisplayOtherFull + pData->fDisplayRawData);
    byte fDisplayRawData  = pData->fDisplayRawData;

        // la base ...
    if (! fDisplayHeader) return;


    raw = pData->raw;
    if (caller[0] == 'T')
        data = pData->tx;
    else if (caller[0] == 'R')
        data = pData->rx;
    else
        return;



    // if (( ! pData->fDisplayOtherData) && (!isItForMe) )
    //     return;


    byte dataLen = data[fld_DATALEN];
    byte rawLen  = raw[0];


    if (dataLen > 0) {
        int seqNo = data[fld_SEQNO_LOW] + data[fld_SEQNO_HIGH]*256;
        /* ------- sample output
            [Slave-011] - RX-data - 0x00 --> 0x0B - SeqNO: 00001 - [WOW it's for me...] - [rcvdCode: OK]

            fullData    hex - len:[022] - 00 0B 00 01 00 02 01 50 6F 6C 6C 69 6E 67 20 72 65 71 75 65 73 74
            commandData hex - len:[015] -                      50 6F 6C 6C 69 6E 67 20 72 65 71 75 65 73 74
            commandData asc - len:[015] -                      [Polling request]

            CRC Rec/Cal 0x : 57 57
            SEQNO       0x : 00 01
            CMD_RCode   0x : 00
            CMD/subCMD  0x : 02 01
        ------- sample output --------- */

        // --- HEADER START -----
        if (fDisplayHeader) {
            Serial.println();
            Serial.print(pData->myID);
                Serial.print(caller);
                Serial.print(F(" - 0x"));       printHex(data[fld_SENDER_ADDR]);
                Serial.print(F("-->0x"));       printHex(data[fld_DESTINATION_ADDR]);
                Serial.print(F(" - SeqNO: "));  Serial.print(Utoa(seqNo, 5, '0') );

                // - Occupa molta più memoria (almeno 150 byte in più)
                    // char *ptr = joinStr(pData->myID, caller, " - 0x", D2X(data[fld_SENDER_ADDR], 2), " --> 0x",D2X(data[fld_DESTINATION_ADDR], 2), "/",Utoa(data[fld_DESTINATION_ADDR], 3, '0'),"] - SeqNO: ", Utoa(seqNo, 5, '0'), NULL);
                    // Serial.print(ptr);

                byte isItForMe = (pData->myEEpromAddress == data[fld_DESTINATION_ADDR]) + (pData->myEEpromAddress == data[fld_SENDER_ADDR]);
                if (isItForMe) {
                    Serial.print(F(" - [WOW it's for me...]"));
                    fDisplayFullData = true;
                }
                else {
                    Serial.print(F(" - [it's NOT for me...]"));
                    if (pData->fDisplayOtherFull) fDisplayFullData = true;
                }

                if (caller[0] == 'R') {
                    Serial.print(F(" - [rcvdCode: "));
                    Serial.print(errMsg[rCode]);
                    Serial.print(']');
                }
        } // --- HEADER END -----


        if (fDisplayFullData) {
            Serial.println();

                // print dataLen
            Serial.print(TAB4);Serial.print(F("fullData    hex - len:["));Serial.print(Utoa(dataLen, 3, '0'));Serial.print(F("] - "));
                // FULL COMMAND DATA (inclusi SA, DA, etc..
            printHex((char *) &data[fld_DATALEN+1], data[fld_DATALEN]);

            // DATA_COMMAND
            byte lun=dataLen-fld_SUBCOMMAND;
            Serial.print(TAB4);Serial.print(F("commandData hex - len:["));Serial.print(Utoa(lun, 3, '0'));Serial.print(F("] - "));
                printNchar(' ', fld_SUBCOMMAND*3);printHex((char *) &data[fld_DATA_COMMAND], lun);

            Serial.print(TAB4);Serial.print(F("commandData asc - len:["));Serial.print(Utoa(lun, 3, '0'));Serial.print(F("] - "));
                printNchar(' ', fld_SUBCOMMAND*3); printDelimitedStr((char *) &data[fld_DATA_COMMAND], lun, "[]");

            Serial.println();
            if (caller[0] == 'R') {
                Serial.print(TAB4);Serial.print(F( "CRC Rec/Cal 0x : "));printHex(pData->Rx_CRCrcvd);Serial.print(" ");printHex(pData->Rx_CRCcalc);
            }
            else {
                Serial.print(TAB4);printHexPDS(    "xMitted CRC 0x : ", pData->Tx_CRCcalc, "");
            }

            Serial.print(TAB4);Serial.print(F( "SEQNO       0x : "));printHex((char *) &data[fld_SEQNO_HIGH], 2);
            Serial.print(TAB4);Serial.print(F( "CMD_RCode   0x : "));printHex(data[fld_CMD_RCODE]);
            Serial.print(TAB4);Serial.print(F( "CMD/subCMD  0x : "));printHex(data[fld_COMMAND]);Serial.print(" ");printHex(data[fld_SUBCOMMAND]);

        } // end fDisplayFullData
    }   // end dataLen


    if (fDisplayRawData) {
        if (rawLen > 0) {
            rawIndex = fld_DATA_COMMAND*2;
            Serial.println();
            Serial.print(TAB4);Serial.print(F("full raw - len:["));Serial.print(Utoa(raw[0], 3, '0'));Serial.print(F("] - "));
            Serial.print(TAB4);printHex((char *) &raw[1], raw[0]); //Serial.println();

            Serial.println();
            Serial.print(TAB4);Serial.print(F("CMD  raw -      "));;Serial.print(Utoa(raw[0], 3, '0'));
            Serial.print(TAB4);printHex((char *) &raw[rawIndex], rawLen-rawIndex-2);//Serial.println();

        }
    }
    // printHexPDS( "calculated CRC3b: ", pData->Tx_CRCcalc, "\n");
}




