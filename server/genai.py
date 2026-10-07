"""Gen AI layer: turns raw detections + sensor data into caregiver-friendly text."""
import requests
from config import GEMINI_API_KEY, GEMINI_MODEL

URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
client = GEMINI_API_KEY or None  # None -> use template messages


def _ask(prompt, max_tokens=400):
    r = requests.post(
        URL,
        headers={"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY},
        json={"contents": [{"parts": [{"text": prompt}]}],
              "generationConfig": {"maxOutputTokens": max_tokens}},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


def build_alert(label, confidence, sensor, time_str):
    fallback = f"Alert: {label} detected ({confidence:.0%}) at {time_str}. Please check."
    if client is None:
        return fallback
    prompt = (
        "You are a care assistant for a baby/elderly monitoring system.\n"
        f"Detected sound: {label} (confidence {confidence:.0%}) at {time_str}.\n"
        f"Room sensors: {sensor or 'not available'}.\n"
        "Write a calm alert of at most 3 short lines for the caregiver. "
        "Suggest 2 possible causes or checks using the room data. "
        "Do not make medical claims or diagnoses."
    )
    try:
        return _ask(prompt)
    except Exception as e:
        print("LLM error, using fallback:", e)
        return fallback


def daily_summary(events):
    if not events:
        return "No events recorded."
    lines = "\n".join(f"{e['time']}: {e['label']} ({e['confidence']:.0%})" for e in events)
    fallback = f"{len(events)} events recorded today."
    if client is None:
        return fallback
    try:
        return _ask("Summarise these monitoring events for a caregiver in 4 lines, "
                    "noting any pattern:\n" + lines, max_tokens=250)
    except Exception as e:
        print("LLM error:", e)
        return fallback
