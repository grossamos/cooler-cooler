#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp; // I2C

void init_sensor() {
  unsigned status;
  do {
    status = bmp.begin(0x76);
    if (!status) {
      Serial.printf("[BMP] Failed to find sensor, sensorID is %x (0 implies not found)\n", bmp.sensorID());
      delay(2000);
    }
  } while (!status);
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}


double get_temperature() {
  return bmp.readTemperature();
}