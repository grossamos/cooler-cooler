#include <Arduino.h>
#include "secrets.h"

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(921600);
}

void loop() {
  delay(1000);
  Serial.println("Hello World!");
  digitalWrite(LED_BUILTIN, LOW);
  delay(5000);
  digitalWrite(LED_BUILTIN, HIGH);
}