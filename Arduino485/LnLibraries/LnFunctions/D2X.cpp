#include <LnFunctions.h>                //  D2X(dest, val, 2)


char D2Xbuffer[10];


char *D2X(unsigned int Valore, char size) {
    char HexStr[] = "0123456789ABCDEF";
    const char Base = 16;                        /* Base dei numeri HEX            */
    unsigned int NewVal;
    unsigned int Resto;
    char Byte;
    char *pDest = D2Xbuffer;

    pDest = D2Xbuffer+size;                                        /* andiamo alla fine         */
    *pDest-- = '\0';                                         /* Imposta il fine stringa    */

    do {
        size--;                                    /* Decrementa la LUN              */
        NewVal = Valore/Base;                  /* prendo il nuovo Valore         */
        Resto = (unsigned int) ( Valore - (NewVal*16)); /* Calcolo l'attuale Resto        */
        Byte =  *(HexStr+Resto);             /* lo metto in un char per sicurezza*/
        *pDest-- = Byte;                   /* e lo scivo nella destinazione  */
        Valore = NewVal;                       /* riassegno il nuovo Valore      */
    } while (size!=0);                        /* End for                        */

    return D2Xbuffer;
}