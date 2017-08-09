/*
per compilare c++ online:
    https://www.codechef.com/ide
    https://www.tutorialspoint.com/compile_cpp_online.php   -- anche python

version : LnVer_2017-08-09_15.37.05

*/


#include <LnFunctions.h>                //  D2X(dest, val, 2)


// void joinString(char *returnBuffer, const char *s1, const char *s2, const char *s3, const char *s4 ) {
int joinString(unsigned char *returnBuffer, const char *s1, const char *s2, const char *s3, const char *s4) {
    unsigned char *ptr = returnBuffer;
    const char *str;
    int len = 0;

    str =  s1;
    while (*str) {*ptr++ = *str++; len++; }

    str = s2;
    while (*str) {*ptr++ = *str++; len++; }

    str = s3;
    while (*str) {*ptr++ = *str++; len++; }

    str = s4;
    while (*str) {*ptr++ = *str++; len++; }

    *ptr ='\0'; //fine stringa
    return len;

}



unsigned char *LnUtoa(unsigned int i, byte padLen,  byte fill) {
    unsigned char *p = &LnFuncWorkingBuff[9];
    *p = '\0';                  // chiude il buffer finale

    for(*p--=0; i>0 ;i/=10) {
        *p-- = i%10 + '0';
        padLen--;
        // printf("padLen %i\r\n", padLen);
    }

    // while (padLen--) *p-- = '0';
    while (padLen--) *p-- = fill;

    // printf("%s - %i\r\n", p, padLen);
    return ++p;
}



// ******************************************************************
// * Provvede a concatenare piu' string tra di loro.
// * In un primo giro legge tutte le stringhe per calcolarne la
// * lunghezza totale. Alloca l'area necessaria e poi con un
// * secondo giro provvede a copiare le stringhe nella Destinazione
// *         I M P O R T A N T E
// * Terminare i parametri passati con un NULL
// ******************************************************************
char     *strCatv_OK(byte nArgs,...) {
byte       i;
va_list   vaList;
char      *next;
char *ptr;
char *pNewStr;

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

#define ALLOCATE_MEMORY
// ******************************************************************
// * Provvede a concatenare piu' string tra di loro.
// * In un primo giro legge tutte le stringhe per calcolarne la
// * lunghezza totale. Alloca l'area necessaria e poi con un
// * secondo giro provvede a copiare le stringhe nella Destinazione
// *         I M P O R T A N T E
// * Terminare i parametri passati con un NULL
// ******************************************************************
char  *strCatv2(const char *firstStr,...) { // <------ Ultimo parametro MUST BE NULL
va_list     vaList;
const char  *next;
char        *ptr;
char        *pNewStr;
// int len;


    pNewStr = (char *) LnFuncWorkingBuff;

#ifdef ALLOCATE_MEMORY
int maxLen = 0;
        // -------------------------------------------------------
        // -    G I R O    1
        // - Calcoliamo la lunghezza della stringa
        // - per allocare la memoria per la DEST
        // -------------------------------------------------------

        // - apertura  va_list
    va_start(vaList, firstStr);             // create va_list


        //  for (ptr=next, len=0; *ptr!='\0'; len++, ptr++);
    next = firstStr;                        // la imposto come next per entrare nel loop
    while (next) {
        Serial.print("next: ");Serial.println(next);
        while (*next++) {
            maxLen++;
            Serial.print("maxLen: ");Serial.println(maxLen);
        }
        next = va_arg(vaList, const char *);             // get next pointer
    }
    Serial.print("maxLen: ");Serial.println(maxLen);
    va_end(vaList);

        // - allocazione memoria
    pNewStr = (char *) malloc(maxLen+1);         // Alloc new Area
    if (pNewStr == NULL) return (NULL);


#endif

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
        Serial.print("next: ");Serial.println(next);
        while (*next) {
            *ptr++ = *next++;                              // copy string
        }
        *ptr ='\0';                                         // close string
        next = va_arg(vaList, const char *);             // get next pointer
    }

    va_end(vaList);

    return pNewStr;
}


#if 0
      // Calcoliamo la lunghezza della stringa
    for (ptr=firstStr, len=0; *ptr != '\0'; len++, ptr++);          // Calculate LEN

 // ------------------- Giro 1 ---------------------------------
    // preleva il primo parametro
    va_start(vaList, firstStr);                                 // Create va_list for variable parameters
    next = va_arg(vaList, char *);                              // get next pointer

   // ----------------------------------------------------
   // finche' troviamo stringhe calcoliamone la lunghezza
   // al fine di trovare la LEN totale.
   // ----------------------------------------------------
   while (next) {
        Serial.print("len:");Serial.println(len);
        next = va_arg(vaList, char *);
   }
   va_end(vaList);
    Serial.print("maxLen:");Serial.println(maxLen);
   pNewStr = (char *) malloc(maxLen);         // Alloc new Area
    Serial.print("maxLen:");Serial.println(maxLen);
   if (pNewStr == NULL) return (NULL);
   ptr = pNewStr;


 // ------------------- Giro 2 ---------------------------------
   // riposizioniamoci all'inizio
   va_start(vaList, firstStr);
   next = firstStr;                                        // la imposto come next per entrare nel loop

   // ----------------------------------------------------
   // finche' abbiamo  stringhe ...
   // Andiamo a copiarle tutte nella Destinazione.
   // ----------------------------------------------------
   while (next) {
      while (*next) {
          *ptr++ = *next++;                              // add string
      }
      next = va_arg(vaList, char *);                           // vai alla next (se c'e')
   }
   va_end(vaList);
   *ptr = '\0';

   return pNewStr;
#endif





#if 0
void
foo(char *fmt, ...)
{
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



// ******************************************************************
// * Provvede a concatenare piu' string tra di loro.
// * In un primo giro legge tutte le stringhe per calcolarne la
// * lunghezza totale. Alloca l'area necessaria e poi con un
// * secondo giro provvede a copiare le stringhe nella Destinazione
// *         I M P O R T A N T E
// * Terminare i parametri passati con un NULL
// ******************************************************************
char     *strCatv(char *firstStr,...) {
int       len = strlen(firstStr);
va_list   ap;
char      *next;
char      *Dest, *pDest;


 // ------------------- Giro 1 ---------------------------------
    // Create va_list for variable parameters
   va_start(ap, firstStr);                                 // Create va_list for variable parameters
   next = va_arg(ap, char *);                              // get next pointer

   // ----------------------------------------------------
   // finche' troviamo stringhe calcoliamone la lunghezza
   // al fine di trovare la LEN totale.
   // ----------------------------------------------------
   while (next) {
       len += strlen(next);
       next = va_arg(ap, char *);
   }

   va_end(ap);

   if ((Dest = (char *) malloc(len+1)) == NULL)
      return (NULL);
   pDest = Dest;

 // ------------------- Giro 2 ---------------------------------
   // riposizioniamoci all'inizio
   va_start(ap, firstStr);
   next = firstStr;                                        // la imposto come next per entrare nel loop

   // ----------------------------------------------------
   // finche' abbiamo  stringhe ...
   // Andiamo a copiarle tutte nella Destinazione.
   // ----------------------------------------------------
   while (next) {
      while (*next) {
          *pDest++ = *next++;                              // add string
      }
      next = va_arg(ap, char *);                           // vai alla next (se c'e')
   }
   //va_end(ap);
   *pDest = '\0';

   return Dest;
}
#endif