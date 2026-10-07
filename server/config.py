import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8857581032:AAF3uq9omcTNsxSPmzYeJKZjj6XZOBZddNs")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1252149296")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDJYRXhOx_NY0j7OVQOYovP-BzcW0XfEro")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

# Audio detection
SAMPLE_RATE = 16000
WINDOW_SEC = 3
THRESHOLD = 0.35        # lower = more sensitive
COOLDOWN_SEC = 60       # minimum gap between alerts of the same type

# YAMNet class name -> friendly label
WATCH = {
    "Baby cry, infant cry": "Baby crying",
    "Crying, sobbing": "Someone crying",
    "Cough": "Coughing",
    "Shatter": "Glass breaking",
    "Screaming": "Screaming",
    "Yell": "Shouting for help",
}
