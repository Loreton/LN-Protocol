/*
    http://www.gammon.com.au/forum/?id=11428
*/
#include <SoftwareSerial.h>
#include "RS485_protocol.h"

SoftwareSerial rs485 (2, 3);  // receive pin, transmit pin
const byte ENABLE_PIN = 4;

void fWrite (const byte what)
  {
  rs485.write (what);
  }

int fAvailable ()
  {
  return rs485.available ();
  }

int fRead ()
  {
  return rs485.read ();
  }

void setup()
{
  rs485.begin (28800);
  pinMode (ENABLE_PIN, OUTPUT);  // driver output enable
}

void loop()
{
  byte buf [10];

  byte received = recvMsg (fAvailable, fRead, buf, sizeof (buf));

  if (received)
    {
    if (buf [0] != 1)
      return;  // not my device

    if (buf [1] != 2)
      return;  // unknown command

    byte msg [] = {
       0,  // device 0 (master)
       3,  // turn light on command received
    };

    delay (1);  // give the master a moment to prepare to receive
    digitalWrite (ENABLE_PIN, HIGH);  // enable sending
    sendMsg (fWrite, msg, sizeof msg);
    digitalWrite (ENABLE_PIN, LOW);  // disable sending

    analogWrite (11, buf [2]);  // set light level
   }  // end if something received

}  // end of loop