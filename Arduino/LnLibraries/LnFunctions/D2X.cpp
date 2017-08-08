#include <LnFunctions.h>                //  D2X(dest, val, 2)

#if 0
void D2X(char *Dest, unsigned int Valore, char size) {
// 2017-03-19 18.30.11 from char *HexStr = "0123456789ABCDEF"; to char HexStr[] = "0123456789ABCDEF";
char HexStr[] = "0123456789ABCDEF";
const char Base = 16;                        /* Base dei numeri HEX            */
unsigned int NewVal;
unsigned int Resto;
char Byte;
// char *Dest = "0000000000";
char *pDest;

    pDest = Dest+size;                                        /* andiamo alla fine         */
    *pDest-- = '\0';                                         /* Imposta il fine stringa    */

    do {
        size--;                                    /* Decrementa la LUN              */
        NewVal = Valore/Base;                  /* prendo il nuovo Valore         */
        Resto = (unsigned int) ( Valore - (NewVal*16)); /* Calcolo l'attuale Resto        */
        Byte =  *(HexStr+Resto);             /* lo metto in un char per sicurezza*/
        *pDest-- = Byte;                   /* e lo scivo nella destinazione  */
        Valore = NewVal;                       /* riassegno il nuovo Valore      */
    } while (size!=0);                        /* End for                        */

    return;
}
#endif


unsigned char *D2X(unsigned int Valore, char size) {
// 2017-03-19 18.30.11 from char *HexStr = "0123456789ABCDEF"; to char HexStr[] = "0123456789ABCDEF";
char HexStr[] = "0123456789ABCDEF";
const char Base = 16;                        /* Base dei numeri HEX            */
unsigned int NewVal;
unsigned int Resto;
char Byte;
// char *Dest = "0000000000";
unsigned char *pDest = LnFuncWorkingBuff;

    pDest = LnFuncWorkingBuff+size;                                        /* andiamo alla fine         */
    *pDest-- = '\0';                                         /* Imposta il fine stringa    */

    do {
        size--;                                    /* Decrementa la LUN              */
        NewVal = Valore/Base;                  /* prendo il nuovo Valore         */
        Resto = (unsigned int) ( Valore - (NewVal*16)); /* Calcolo l'attuale Resto        */
        Byte =  *(HexStr+Resto);             /* lo metto in un char per sicurezza*/
        *pDest-- = Byte;                   /* e lo scivo nella destinazione  */
        Valore = NewVal;                       /* riassegno il nuovo Valore      */
    } while (size!=0);                        /* End for                        */

    return LnFuncWorkingBuff;
}