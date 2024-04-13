import time

from app.models import ActivityLog


def generate_facebook_event_data(activity_log: ActivityLog, status: str, value: int = 200):
    current_timestamp = int(time.time())
    user_data = {
        "client_ip_address": str(activity_log.ip_address),
        "client_user_agent": activity_log.user_agent,
        "fbc": activity_log.fbc,
        "fbp": activity_log.fbp,
    }
    if status == "lead":
        event_name = "Lead"
        action_source = "chat"
    else:
        event_name = "Purchase"
        action_source = "website"
        user_data.update({"custom_data": {"currency": "USD", "value": value}})

    event_data = {
        "data": [
            {
                "event_name": event_name,
                "event_time": current_timestamp,
                "action_source": action_source,
                "user_data": user_data,
            }
        ]
    }
    return event_data
