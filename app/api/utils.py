import time

from app.models import ActivityLog

LEAD = "lead"
SALE = "sale"


def generate_facebook_event_data(activity_log: ActivityLog, status: str = "flow_matched", value: int = 200):
    current_timestamp = int(time.time())
    user_data = {
        "client_ip_address": str(activity_log.ip_address),
        "client_user_agent": activity_log.user_agent,
        "fbc": activity_log.fbc,
        "fbp": activity_log.fbp,
    }
    if status == LEAD:
        event_name = "CompleteRegistration"
        action_source = "website"
        del user_data["fbp"]
    elif status == SALE:
        event_name = "Purchase"
        action_source = "website"
    elif status == "flow_matched":
        event_name = LEAD.capitalize()
        action_source = "chat"

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
    if status in [SALE, LEAD]:
        event_data["data"][0]["custom_data"] = {"currency": "USD", "value": value}
    return event_data
