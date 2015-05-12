
#include <LnFunctions.h>                //  D2X(dest, val, 2)
#include <RS485_protocol.h>
#include <RS485_non_blocking.h>
#include <SoftwareSerial.h>


// const byte ENABLE_PIN   =  4;
#define ENABLE_PIN      3
#define LED_PIN        13
#define RX_PIN         10
#define TX_PIN         11

const byte myADDR       = 2;
const char *devName     = "[Slave02]";
int nLoops              = 0;
bool fDEBUG             = true;
unsigned long timeOUT   = 10000;

// --------------------
//     mi serve per verificare i dati e l'ordine con cui sono
//     stati inviati inclusi STX, CRC, ETX
//     DEBUG_sentMsg[0] contiene lunghezza dei dati
// --------------------
byte DEBUG_TxRxMsg [200] = "                                                                ";   // gli faccio scrivere il messaggio inviato con relativo CRC

