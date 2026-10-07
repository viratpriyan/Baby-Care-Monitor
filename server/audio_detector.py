"""Microphone -> YAMNet (pretrained) -> calls callback(label, confidence)."""
import csv
import time
import sounddevice as sd
import tensorflow_hub as hub
from config import SAMPLE_RATE, WINDOW_SEC, THRESHOLD, COOLDOWN_SEC, WATCH


def run(callback):
    print("Loading YAMNet (needs internet on first run)...")
    model = hub.load("https://tfhub.dev/google/yamnet/1")
    with open(model.class_map_path().numpy().decode()) as f:
        names = [row["display_name"] for row in csv.DictReader(f)]
    watch_idx = {names.index(k): v for k, v in WATCH.items() if k in names}
    last_alert = {}

    print("Listening...")
    while True:
        audio = sd.rec(int(WINDOW_SEC * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                       channels=1, dtype="float32")
        sd.wait()
        scores, _, _ = model(audio[:, 0])
        mean_scores = scores.numpy().mean(axis=0)

        for idx, label in watch_idx.items():
            conf = float(mean_scores[idx])
            if conf >= THRESHOLD and time.time() - last_alert.get(label, 0) > COOLDOWN_SEC:
                last_alert[label] = time.time()
                callback(label, conf)
