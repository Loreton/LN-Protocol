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

// ******************************************************************
// * Provvede a stampare piu' dati.
// * Come primo parametro il numero di argomenti passati
// ---  https://linux.die.net/man/3/va_start
// ******************************************************************
void foo(char *fmt, ...) {
    va_list ap;
    int d;
    char c, *s;

    va_start(ap, fmt);
        while (*fmt)
            switch (*fmt++) {
            case 's':              /* string */
                s = va_arg(ap, char *);
                printf("string %s\n", s);
                break;
            case 'd':              /* int */
                d = va_arg(ap, int);
                printf("int %d\n", d);
                break;
            case 'c':              /* char */
                /* need a cast here since va_arg only
                   takes fully promoted types */
                c = (char) va_arg(ap, int);
                printf("char %c\n", c);
                break;
            }
    va_end(ap);
}