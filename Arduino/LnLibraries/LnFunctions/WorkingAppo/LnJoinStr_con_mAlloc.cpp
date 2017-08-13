/*
per compilare c++ online:
    https://www.codechef.com/ide
    https://www.tutorialspoint.com/compile_cpp_online.php   -- anche python

version : LnVer_2017-08-10_07.49.51

*/


#include <LnFunctions.h>                //  D2X(dest, val, 2)


#define USE_MEMORY_ALLOC
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
unsigned long MAX_MEM = 0;

char  *LnJoinStr(const char *firstStr,...) { // <------ Ultimo parametro MUST BE NULL
va_list     vaList;
const char  *next;
char        *ptr;
char        *pNewStr;



    // pNewStr = (char *) LnFuncWorkingBuff;
    pNewStr = sharedWorkingBuff;

#ifdef USE_MEMORY_ALLOC
int maxLen = 0;

        // -------------------------------------------------------
        // -    G I R O    1
        // -------------------------------------------------------
        // - apertura  va_list
    va_start(vaList, firstStr);             // create va_list

        // -------------------------------------------------------
        // - Calcoliamo la lunghezza della stringa
        // - per allocare la memoria per la DEST
        //  for (ptr=next, len=0; *ptr!='\0'; len++, ptr++);
        // -------------------------------------------------------
    next = firstStr;                        // la imposto come next per entrare nel loop
    while (next) {
        // Serial.print("next: ");Serial.println(next);
        while (*next++) {
            maxLen++;
            MAX_MEM += maxLen;
            // Serial.print("maxLen: ");Serial.println(maxLen);
        }
        next = va_arg(vaList, const char *);             // get next pointer
    }
    // Serial.print("maxLen: ");Serial.println(maxLen);
    va_end(vaList);

        // - allocazione memoria
    pNewStr = (char *) malloc(maxLen+1);         // Alloc new Area
    if (pNewStr == NULL) return (NULL);


#endif

    Serial.print("MAX_MEM: ");Serial.println(MAX_MEM);
    ptr = pNewStr;


        // -------------------------------------------------------
        // -    G I R O    2
        // - copia delle stringhe nel destination buffer
        // -------------------------------------------------------

    va_start(vaList, firstStr);             // create va_list
        // ----------------------------------------------------
        // finche' abbiamo  stringhe ...
        // Andiamo a copiarle tutte nella Destinazione.
        // ----------------------------------------------------
    next = firstStr;                        // la imposto come next per entrare nel loop
    while (next) {
           /* access all the arguments assigned to vaList */
        // Serial.print("next: ");Serial.println(next);
        while (*next) {
            *ptr++ = *next++;                              // copy string
        }
        *ptr ='\0';                                         // close string
        next = va_arg(vaList, const char *);             // get next pointer
    }

    va_end(vaList);

    return pNewStr;
}
