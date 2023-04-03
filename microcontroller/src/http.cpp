
#include <Arduino.h>
#include <HTTPClient.h>

#include "secrets.h"
#include "backend.h"

int upload_temperature(const char* location, float temperature) {
    // ignore really obvious false temperatures
    if (temperature > 60 || temperature < -60) {
        return 0;
    }

    WiFiClientSecure *client = new WiFiClientSecure;
    if (!client) {
        Serial.println("[HTTPS] Unable to create client");
        return 0;
    }
    client -> setCACert(certificate);

    HTTPClient https;
    const char* temperature_url = "/temperature/";
    char* url = (char*) malloc(strlen(base_url) + strlen(temperature_url) + strlen(location) + 1);
    strcpy(url, base_url);
    strcat(url, temperature_url);
    strcat(url, location);

    Serial.printf("[HTTPS] Sending temperature to %s\n", url);

    if (https.begin(*client, url)) {
    https.addHeader("Authorization", BACKEND_CREDENTIAL);

    char payload_buffer[50];
    sprintf(payload_buffer, "{\"temperature\":%f}", temperature);

    int httpCode = https.POST(payload_buffer);
    Serial.printf("[HTTPS] Recieved code: %d\n", httpCode);
    Serial.printf("[HTTPS] Response: \"%s\"\n", https.getString());
    } else {
    Serial.printf("[HTTPS] Unable to connect\n");
    }

    free(url);
    return 1;
}