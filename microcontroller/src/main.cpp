#include <Arduino.h>
#include <HTTPClient.h>

#include "wifi.h"
#include "sensor.h"
#include "http.h"


void setup() {
  Serial.begin(115200);
  while(!Serial){delay(100);}
  
  init_sensor();
  connect_to_wifi();
}

void loop() {
  reconnect_wifi_if_down();
  double temperature = get_temperature();
  if (upload_temperature("inner", temperature)) {
    Serial.printf("[LOOP] Uploaded temperature of %f\n", temperature);
  } else {
    Serial.printf("[LOOP] Upload of temperature of %f failed\n", temperature);
  }
  delay(60000);
}
