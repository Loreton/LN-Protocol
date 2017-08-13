/*
per compilare c++ online:
    https://www.codechef.com/ide
    https://www.tutorialspoint.com/compile_cpp_online.php   -- anche python

version : LnVer_2017-08-10_10.49.13

*/


#include <LnFunctions.h>                //  D2X(dest, val, 2)

// ******************************************************************
// * Provvede a concatenare piu' string tra di loro.
// * Se deve allocare la memoria allora ...
// * 1. legge tutte le stringhe per calcolarne la lunghezza totale.
// * 2. Alloca l'area necessaria
// * 3. secondo giro provvede a copiare le stringhe nella Destinazione
// *         I M P O R T A N T E
// *         I M P O R T A N T E
// *         I M P O R T A N T E
// *    per capire quando sono finiti i parametri....
// * Terminare i parametri passati con un NULL
// * Terminare i parametri passati con un NULL
// * Terminare i parametri passati con un NULL
// * Terminare i parametri passati con un NULL
// ******************************************************************
#define USE_MEMORY_ALLOCxxx
#define MAX_LEN  100
char joinStrBuffer[MAX_LEN]; // 50 bytes
char *prevString;


// - Ho notato che chiamarla occupa più memoria che non fare le print specifiche...
// - ... quindi valutare...
char  *joinStr(const char *firstStr,...) { // <------ Ultimo parametro MUST BE NULL
va_list     vaList;
const char  *next;
char        *ptr;
char        *pReturnData;
byte         MAX_MEM = 0;



    ptr = joinStrBuffer;

        // -------------------------------------------------------
        // - copia delle stringhe nel destination buffer
        // -------------------------------------------------------
    va_start(vaList, firstStr);             // create va_list
        // ----------------------------------------------------
        // Andiamo a copiarle tutte nella Destinazione.
        // finche' abbiamo  stringhe ...
        // ... e finche' non riempiamo il buffer ...
        // ----------------------------------------------------

    next = firstStr;                        // la imposto come next per entrare nel loop
    while ( (next) && (MAX_MEM < MAX_LEN)) {
           // access all the arguments assigned to vaList
        while ( (*next) && (MAX_MEM < MAX_LEN)) {
            MAX_MEM++;   // contiamo i bytes letti
            *ptr++ = *next++;                              // copy string
        }
        next = va_arg(vaList, const char *);             // get next pointer
    }

    *ptr ='\0';                                         // close string
    va_end(vaList);
    pReturnData = joinStrBuffer;      // pointer da tornare



        // a questo punto possiamo decidere se allocare o meno la memoria...
#ifdef USE_MEMORY_ALLOC

        // Se la allochiamo allora cerchiamo di prendere
        // blocchi a boundary di 10 bytes
    Serial.print("\n\rMAX_MEM: ");Serial.println(MAX_MEM);
    int nBytes = ((MAX_MEM/10)+1)*10;
    Serial.print("nBytes : ");Serial.println(nBytes);

    char *newStr = (char *) malloc(nBytes);         // Alloc new Area
    if (newStr) {       // allocazione OK
        char *ptrTo     = newStr;
        char *ptrFrom   = joinStrBuffer;
        while (*ptrFrom) {
            *ptrTo++ = *ptrFrom++;                              // copy string
        }
        *ptrTo = '\0';                                         // close string
        pReturnData = newStr;      // pointer da tornare
    }
    else {
        return ((char *)"ERRORE di allocazione memoria");
    }

    // liberiamo la memoria precedente (okkio!!!! dobbiamo essere consapevoli del rischio)
    if (prevString) free(prevString);
    prevString = pReturnData;

#endif

    return pReturnData;
}
