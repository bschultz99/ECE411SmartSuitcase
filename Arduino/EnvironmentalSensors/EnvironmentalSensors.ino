#include <Wire.h>
#include "Adafruit_VEML6070.h" //UV Sensor
#include "Adafruit_SGP30.h" //Gas Sensor
#include "DHT.h"

DHT dht(2, DHT11);
Adafruit_SGP30 sgp;

Adafruit_VEML6070 uv = Adafruit_VEML6070();

void setup() {
  Serial.begin(9600); //Baud Rate of 9600
  while (!Serial) { delay(10); } //Delay to allow communication to be established
  if (! sgp.begin()){
    Serial.println("Sensor not found :(");
    while (1);
  }
  dht.begin();
  uv.begin(VEML6070_1_T);
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if( isnan(h) || isnan(t)){
    Serial.println("DHT Failed");
    return;
  }
  if (! sgp.IAQmeasure()) {
    Serial.println("Measurement failed");
    return;
  }
  Serial.print("TVOC "); Serial.print(sgp.TVOC); Serial.print(" ppb\t"); //Total Volatile Organic Compounds
  Serial.print("eCO2 "); Serial.print(sgp.eCO2); Serial.println(" ppm"); //Equivalent Carbon Dioxide Reading
  if (! sgp.IAQmeasureRaw()) {
    Serial.println("Raw Measurement failed");
    return;
  }
  Serial.print("Raw H2 "); Serial.print(sgp.rawH2); Serial.print(" \t"); //H2 concentration
  Serial.print("Raw Ethanol "); Serial.print(sgp.rawEthanol); Serial.println(""); //Ethanol concentration
  delay(1000);
  Serial.print("UV light level: "); Serial.println(uv.readUV()); //UV light level
  delay(1000);
  Serial.print("Humidity: "); Serial.print(h); Serial.println(""); //Humidity
  Serial.print("Temperature: "); Serial.print(t); Serial.println(""); //Temperature
}
