"""Pure input validation helpers, kept independent of the GUI for testing."""
import re
from datetime import datetime

_PHONE_RE = re.compile(r"^\+[1-9]\d{7,14}$")


def normalize_phone(value: str) -> str:
    """Validate an international E.164-style number and return its trimmed form."""
    phone = value.strip()
    if not _PHONE_RE.fullmatch(phone):
        raise ValueError("Use international phone format, e.g. +254712345678.")
    return phone


def validate_recipients(raw: str) -> list[str]:
    recipients = [part.strip() for part in raw.split(",") if part.strip()]
    if not recipients:
        raise ValueError("Enter at least one recipient phone number.")
    normalized = [normalize_phone(number) for number in recipients]
    if len(set(normalized)) != len(normalized):
        raise ValueError("Duplicate recipient numbers were entered.")
    return normalized


def validate_message(value: str) -> str:
    message = value.strip()
    if not message:
        raise ValueError("Message cannot be empty.")
    # Prevent accidental format-string crashes for unsupported placeholders.
    try:
        message.format(name="Example")
    except (KeyError, ValueError, IndexError) as exc:
        raise ValueError("Use only the supported {name} placeholder, with balanced braces.") from exc
    return message


def validate_daily_time(value: str) -> str:
    candidate = value.strip()
    try:
        datetime.strptime(candidate, "%H:%M")
    except ValueError as exc:
        raise ValueError("Enter a valid 24-hour time in HH:MM format.") from exc
    return candidate
