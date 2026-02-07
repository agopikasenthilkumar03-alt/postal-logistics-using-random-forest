from datetime import datetime

from app.core.config import settings


def build_delay_message(delay_days: int) -> str:
    return f"Due to adverse weather conditions, your post delivery is delayed by {delay_days} days."


def send_sms(phone_number: str, message: str) -> dict:
    # Placeholder for SMS provider integration (Twilio, etc.)
    # This function is called only after admin approval.
    return {
        "provider": settings.sms_provider,
        "to": phone_number,
        "message": message,
        "sent_at": datetime.utcnow().isoformat(),
        "provider_reference": f"mock-{phone_number[-4:]}",
    }
