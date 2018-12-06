/*
 * Scrive la temperatura corrente in gradi Celsius * 10
 * nell'output seriale una volta al minuto; l'output
 * è composto da righe del tipo "temp_c=103", senza
 * le virgolette.
 */

#include <stdio.h>
#include <math.h>
#include "DHT.h"
 
#define DHTPIN 2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)

DHT dht(DHTPIN, DHTTYPE);

int temperature;
int humidity;
int count;
char row[50];

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  temperature = 0;
  humidity = 0;
  count = 0;
  for (int i = 0; i < 20; i++) {
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (!isnan(h) && !isnan(t)) {
      temperature += (int) (t * 10);
      humidity += (int) h;
      count++;        
    }
    delay(2750);
  }
  temperature /= count;
  humidity /= count;

  sprintf(row, "%d;%d\n", temperature, humidity);
  Serial.print(row);
}
