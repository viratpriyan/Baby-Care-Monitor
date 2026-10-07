"""Main server: receives ESP32 sensor data, runs audio AI, builds Gen AI alerts."""
import threading
from datetime import datetime
from flask import Flask, request, jsonify

import audio_detector
import database
import genai
from notifier import send_telegram

app = Flask(__name__)
latest_sensor = {}
lock = threading.Lock()


@app.route("/sensor", methods=["POST"])
def sensor():
    data = request.get_json(force=True)
    with lock:
        latest_sensor.clear()
        latest_sensor.update(data)
        latest_sensor["received"] = datetime.now().strftime("%H:%M:%S")
    return jsonify(ok=True)


@app.route("/status")
def status():
    with lock:
        return jsonify(latest_sensor)


@app.route("/summary")
def summary():
    return jsonify(summary=genai.daily_summary(database.today_events()))


def handle_event(label, confidence):
    """Called by the audio detector: fuse with sensors -> Gen AI -> alert -> log."""
    with lock:
        sensor_now = dict(latest_sensor)
    time_str = datetime.now().strftime("%I:%M %p")
    alert = genai.build_alert(label, confidence, sensor_now, time_str)
    send_telegram(alert)
    database.log_event(label, confidence, sensor_now, alert)
    print(f"[{time_str}] {label} ({confidence:.0%})\n{alert}\n")


if __name__ == "__main__":
    database.init()
    threading.Thread(target=audio_detector.run, args=(handle_event,), daemon=True).start()
    app.run(host="0.0.0.0", port=5001)
