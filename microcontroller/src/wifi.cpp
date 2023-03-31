#include <Arduino.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <WiFiClientSecure.h>

#include "secrets.h"

void set_clock() {
  configTime(0, 0, "pool.ntp.org");

  Serial.print(F("[WiFi] Waiting for NTP time sync: "));
  time_t nowSecs = time(nullptr);
  while (nowSecs < 8 * 3600 * 2) {
    delay(500);
    Serial.print(F("."));
    yield();
    nowSecs = time(nullptr);
  }

  Serial.println();
  struct tm timeinfo;
  gmtime_r(&nowSecs, &timeinfo);
  Serial.print(F("[WiFi] Current time: "));
  Serial.print(asctime(&timeinfo));
}

WiFiMulti wifiMulti;

void reconnect_wifi_if_down() {
    while (WiFi.status() != WL_CONNECTED) {
        Serial.println("[WiFi] Connection lost, reconnecting...");
        WiFi.disconnect();
        WiFi.reconnect();
        delay(5000);
    }
    Serial.println("[WiFi] Connected.");
}

void connect_to_wifi() {
  WiFi.mode(WIFI_STA);

  Serial.printf("[WiFi] Connecting to %s ...", SSID);
  WiFi.begin(SSID, PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\n[WiFi] Connected");

  // set clock for date validity checks in certificates
  set_clock();
}