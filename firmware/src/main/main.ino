// ESP32: reads External Microphone (sound)
// and POSTs JSON to the Python server every 10 seconds.
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

// ---------- CHANGE THESE ----------
const char* WIFI_SSID = "Aravind S P";
const char* WIFI_PASS = "1a2b3c4d5";
const char* SERVER_URL = "http://10.231.14.206:5001/sensor"; // laptop IP
// ----------------------------------

#define MIC_PIN 34              // Analog pin for External Mic (MAX9814 / KY-037 / KY-038)
#define SOUND_THRESHOLD 2000    // Adjust sensitivity threshold (ADC range: 0-4095)
#define SEND_INTERVAL_MS 10000

unsigned long lastSend = 0;
int soundSeen = 0;    // latched until next send
int maxSoundVal = 0;  // peak analog reading

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
  pinMode(MIC_PIN, INPUT);
  connectWiFi();
}

void loop() {
  // Sample external microphone analog sound level
  int micVal = analogRead(MIC_PIN);
  if (micVal > maxSoundVal) maxSoundVal = micVal;
  if (micVal >= SOUND_THRESHOLD) soundSeen = 1;

  if (millis() - lastSend >= SEND_INTERVAL_MS) {
    lastSend = millis();
    
    if (WiFi.status() != WL_CONNECTED) connectWiFi();

    String json = "{\"sound\":" + String(soundSeen) +
                  ",\"sound_val\":" + String(maxSoundVal) + "}";
    HTTPClient http;
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");
    int code = http.POST(json);
    Serial.println("POST " + json + " -> HTTP " + String(code));
    http.end();

    soundSeen = 0;
    maxSoundVal = 0;
  }
  delay(50);
}
