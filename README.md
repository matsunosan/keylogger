# Keylogger and Screenshot Capture Script

This script logs user keystrokes and captures screenshots at regular intervals. It also sends these logs and screenshots via email to a configured address.

## Features
- **Keystroke Logging:** Logs both regular keys (letters, numbers) and special keys (Ctrl, Shift, Enter, etc.) in a readable format.
- **Screenshot Capture:** Takes screenshots every 5 minutes (default) and saves them to a `screenshots` folder.
- **Email Logs:** Automatically sends the keystrokes and screenshots to the configured email address every hour (default).

## How to Use

1. **Install Dependencies:**
    ```bash
    pip install pynput Pillow
    ```

2. **Configure Email Settings:**
    Create a `config/email_config.json` file with your email settings:
    ```json
    {
        "sender_email": "youremail@example.com",
        "receiver_email": "receiver@example.com",
        "smtp_server": "smtp.example.com",
        "smtp_port": 587,
        "password": "your_email_password"
    }
    ```

3. **Run the Script:**
    ```bash
    python keylogger.py
    ```

## Notes
- The script logs both character keys and special keys in a user-friendly format.
- All screenshots are saved in the `screenshots` directory.
- Keystrokes are saved in a `keystrokes.txt` file.
