import cv2
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import threading
import time
import os
from datetime import datetime, timedelta
#from google.cloud import storage
#from telegram import Bot

class SecurityCam:
    def __init__(self,
                 video_dir='recordings',
                 fps=20,
                 post_motion_minutes=1,
                 use_gcs=True,
                 use_telegram=True):

        self.video_dir = video_dir
        os.makedirs(video_dir, exist_ok=True)
        self.fps = fps
        self.motion_threshold = 50000
        self.recording = False
        self.motion_detected = False
        self.last_motion_time = None
        self.post_motion_seconds = post_motion_minutes * 60
        #self.use_telegram = use_telegram
        self.use_gcs = use_gcs

        #if self.use_telegram:
            #self.bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'
            #self.chat_id = 'YOUR_TELEGRAM_CHAT_ID'
            #self.bot = Bot(token=self.bot_token)

        #if self.use_gcs:
            #self.bucket_name = 'YOUR_BUCKET_NAME'
            #self.gcs_client = storage.Client()

        self.cap = cv2.VideoCapture(0)

    def detect_motion(self, frame1, frame2):
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        return np.sum(thresh) > self.motion_threshold

    def record_audio(self, filename, duration):
        fs = 44100
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        wav.write(filename, fs, audio_data)

    #def send_telegram_alert(self, message):
    #    if self.use_telegram:
    #        self.bot.send_message(chat_id=self.chat_id, text=message)

    #def upload_to_gcs(self, local_path):
    #    if not self.use_gcs:
    #        return None
    #    blob_name = os.path.basename(local_path)
    #    bucket = self.gcs_client.bucket(self.bucket_name)
    #    blob = bucket.blob(blob_name)
    #    blob.upload_from_filename(local_path)
    #    return f"https://storage.googleapis.com/{self.bucket_name}/{blob_name}"

    def start_recording(self):
        self.recording = True
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        video_filename = os.path.join(self.video_dir, f"{timestamp}.avi")
        audio_filename = os.path.join(self.video_dir, f"{timestamp}.wav")

        width = int(self.cap.get(3))
        height = int(self.cap.get(4))
        out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), self.fps, (width, height))

        audio_thread = threading.Thread(target=self.record_audio, args=(audio_filename, self.post_motion_seconds + 10))
        audio_thread.start()

        print("[INFO] Recording started")
        #self.send_telegram_alert("🚨 Motion detected! Recording started.")

        start_time = time.time()

        while True:
            ret, frame = self.cap.read()
            if ret:
                out.write(frame)

            if time.time() - self.last_motion_time.timestamp() > self.post_motion_seconds:
                break
            time.sleep(1 / self.fps)

        out.release()
        self.recording = False

        if self.use_gcs:
            print("1")
            #video_url = self.upload_to_gcs(video_filename)
            #self.send_telegram_alert(f"🎥 Recording uploaded: {video_url}")
        else:
            #self.send_telegram_alert("🎥 Recording saved locally.")
            print("🎥 Recording saved locally." + video_filename)

        print("[INFO] Recording stopped")

    def run(self):
        ret, frame1 = self.cap.read()
        ret, frame2 = self.cap.read()

        while True:
            if self.detect_motion(frame1, frame2):
                self.motion_detected = True
                self.last_motion_time = datetime.now()
                if not self.recording:
                    threading.Thread(target=self.start_recording).start()

            frame1 = frame2
            ret, frame2 = self.cap.read()

            cv2.imshow("Camera", frame2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    cam = SecurityCam(use_gcs=False, use_telegram=False)  # Change flags here
    cam.run()
