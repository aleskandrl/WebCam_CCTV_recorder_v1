# WebCam-CCTV-recorder-v1
Lightweight motion-triggered surveillance tool with audio/video recording using webcam, WebCam CCTV recorder, cloud upload, and Telegram alerts. Python-powered and plug-and-play ready.
You can choose to:
- Save files locally
- Upload recordings to Google Cloud Storage
- Get real-time alerts via Telegram

Ideal for basic room surveillance, theft protection, and remote monitoring.


## 🚀 Features

- 🔍 Real-time motion detection via webcam
- 🎥 Video + 🎙️ Audio recording
- 🕒 Extra recording time (5 mins) after motion ends
- ☁️ Optional Google Cloud upload
- 📲 Optional Telegram alerts
- 💽 Local saving option
- 🧱 Object-Oriented Python structure


## ⚙️ Requirements

Install dependencies:

pip install opencv-python numpy sounddevice scipy google-cloud-storage python-telegram-bot

Also make sure you have:
- A working webcam and microphone
- A Google Cloud project with a bucket (if using cloud uploads)
- A Telegram bot and chat ID (if using alerts)

## 🛠 Configuration
In the code, update these variables with your credentials:

- For Telegram
self.bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'
self.chat_id = 'YOUR_TELEGRAM_CHAT_ID'

- For Google Cloud
self.bucket_name = 'YOUR_BUCKET_NAME'

You can enable or disable features when creating the app instance:
cam = SecurityCam(use_gcs=True, use_telegram=True)

## 📦 How to Use
- Connect your webcam and microphone.
- Update the configuration as needed.
- Run the app: python main.py
  
A window will show your camera feed.
The app starts recording when motion is detected.
Recording continues for 5 more minutes after motion stops.

Press Q to quit.

## 🗂 Output
All recordings are saved to the recordings/ folder.
File format: .avi for video and .wav for audio.
If enabled, the app uploads them to Google Cloud and sends a link via Telegram.

## 🧭 Roadmap
Future versions may include:
- Region-of-interest motion zones
- Web GUI for live view and controls
- Email and mobile push alerts
- Multiple camera support

## 📄 License
MIT License — free for personal and commercial use.

