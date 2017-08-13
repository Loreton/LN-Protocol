/*
per compilare c++ online:
    https://www.codechef.com/ide
    https://www.tutorialspoint.com/compile_cpp_online.php   -- anche python

version : LnVer_2017-08-09_15.43.42

*/


#include <LnFunctions.h>                //  D2X(dest, val, 2)


// ******************************************************************
// * Provvede a concatenare piu' string tra di loro.
// * Come primo parametro il numero di argomenti passati
// ---  https://linux.die.net/man/3/va_start
// ******************************************************************
char     *strCatv_with_nArgs(byte nArgs,...) {
byte       i;
va_list   vaList;
char      *next;
char *ptr;
char *pNewStr;

    // destination buffer
    pNewStr = (char *) LnFuncWorkingBuff;
    ptr = pNewStr;

        /* initialize vaList for num number of arguments */
    va_start(vaList, nArgs);

        /* access all the arguments assigned to vaList */
    for (i=0; i<nArgs; i++) {
        next = va_arg(vaList, char *);             // get next pointer
        while (*next) {
            *ptr++ = *next++;                              // add string
        }
        *ptr ='\0';
        Serial.print("pNewStr ");Serial.println(pNewStr);
    }

        /* clean memory reserved for vaList */
    va_end(vaList);

    *ptr = '\0';

    return pNewStr;
}

