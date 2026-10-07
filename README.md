# Acoustic Baby & Elder Care Monitor

ESP32 (DHT22 + PIR) --Wi-Fi--> Flask server <-- YAMNet audio AI (laptop mic)
                                   |
                        Gen AI alert -> Telegram + SQLite log

## Wiring (ESP32)
- DHT22: VCC 3.3V, GND, DATA -> GPIO 4 (10k pull-up between DATA and VCC if bare sensor)
- PIR (HC-SR501): VCC 5V (VIN), GND, OUT -> GPIO 27

## Run
1. Server: cd server; python -m venv venv; activate it; pip install -r ../requirements.txt
   Copy .env.example to .env (in server/) and fill in keys. All are optional: without them
   it prints alerts and uses a template message.
   python app.py
2. Find your laptop IP (ipconfig / ifconfig) and allow port 5000 in the firewall.
3. Firmware: open firmware/ in VS Code with PlatformIO. Edit WIFI_SSID, WIFI_PASS and
   SERVER_URL in src/main.cpp. Upload, then open Serial Monitor.
4. Test: http://localhost:5000/status shows sensor data; play a baby-cry clip near the mic;
   open /summary for the Gen AI daily summary.
