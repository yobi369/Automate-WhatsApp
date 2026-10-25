# WhatsApp Automation Tool

A Python desktop utility for preparing WhatsApp messages, managing contacts, scheduling messages, and recording activity. The UI uses Tkinter, local persistence uses SQLite, and the current sending integration uses PyWhatKit with WhatsApp Web.

> Important: this project automates the WhatsApp Web interface; it is not an official WhatsApp API client. Browser changes, login state, network conditions, and WhatsApp policies can affect operation. An automation call is not proof that a recipient received or read a message. Use only with recipients who have consented. Do not use for spam, unsolicited bulk messaging, or policy evasion.

## Current capabilities

- Tkinter desktop interface
- SQLite persistence for contacts, message logs, and recurring daily schedules
- Restore enabled daily schedules on startup and cancel schedules from the UI
- Message scheduling via the schedule package
- Basic message personalization
- Application logging

## Requirements

- Python 3.10 or newer recommended
- Desktop environment with Tkinter
- WhatsApp Web access and internet connectivity

On Debian/Ubuntu, install Tkinter if needed: `sudo apt install python3-tk`.

## Setup

```bash
git clone https://github.com/yobi369/Automate-WhatsApp.git
cd Automate-WhatsApp
python -m venv .venv
```

Activate the environment: `source .venv/bin/activate` on Linux/macOS, or `.venv\\Scripts\\Activate.ps1` on Windows PowerShell.

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python gui.py
```

## Privacy and local data

The SQLite database and logs are stored locally and may contain phone numbers and message content. Treat them as sensitive, back them up securely, and never commit them to Git. Do not commit browser profiles, QR codes, session data, or secrets.

## Production readiness

This is a desktop utility, not a hosted multi-user messaging service. The current browser-automation integration is fragile and cannot guarantee delivery or account safety. Review `docs/ROADMAP.md` for the work required before production use, especially durable execution/retries, thread safety, consent controls, automated verification, and end-to-end testing. Scheduled times use the computer's local timezone and jobs execute only while the desktop application is running.

For business-critical messaging, evaluate the official WhatsApp Business Platform and its current requirements instead of relying on browser automation.

## Development

Run tests with: `python -m unittest discover -s tests -v`.

See `CONTRIBUTING.md` and `SECURITY.md` for project guidance.

## License

The previous README named a “BML License,” but no license text was present during this update. Reuse and redistribution permissions are therefore unclear. Add a complete license before presenting this repository as open source.
