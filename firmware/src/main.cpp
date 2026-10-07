// ESP32: reads DHT22 (temperature/humidity) + PIR (motion)
// and POSTs JSON to the Python server every 10 seconds.
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// ---------- CHANGE THESE ----------
const char* WIFI_SSID = "Aravind S P";
const char* WIFI_PASS = "1a2b3c4d5";
const char* SERVER_URL = "http://10.231.14.206:5001/sensor"; // laptop IP
// ----------------------------------

#define DHT_PIN 4
#define PIR_PIN 27
#define SEND_INTERVAL_MS 10000

DHT dht(DHT_PIN, DHT22);
unsigned long lastSend = 0;
int motionSeen = 0;  // latched until the next send

void connectWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected. ESP32 IP: " + WiFi.localIP().toString());
}

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  dht.begin();
  connectWiFi();
}

void loop() {
  if (digitalRead(PIR_PIN) == HIGH) motionSeen = 1;

  if (millis() - lastSend >= SEND_INTERVAL_MS) {
    lastSend = millis();
    float t = dht.readTemperature();
    float h = dht.readHumidity();

    if (isnan(t) || isnan(h)) {
      Serial.println("DHT read failed, skipping");
      return;
    }
    if (WiFi.status() != WL_CONNECTED) connectWiFi();

    String json = "{\"temp\":" + String(t, 1) + ",\"hum\":" + String(h, 1) +
                  ",\"motion\":" + String(motionSeen) + "}";
    HTTPClient http;
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");
    int code = http.POST(json);
    Serial.println(json + " -> HTTP " + String(code));
    http.end();
    motionSeen = 0;
  }
  delay(50);
}
