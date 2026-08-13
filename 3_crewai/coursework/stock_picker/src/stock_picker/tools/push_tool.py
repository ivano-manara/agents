from crewai.tools import tool
import requests


NTFY_URL = "https://ntfy.sh/ivano-corso-agents-7f3k2"


@tool("Send Push Notification")
def send_push_notification(message: str) -> str:
    """
    Send a push notification to the user using ntfy.

    Args:
        message: The message to be sent as a push notification.

    Returns:
        A string indicating the status of the notification.
    """
    try:
        response = requests.post(
            NTFY_URL,
            data=message.encode("utf-8"),
            headers={
                "Title": "CrewAI Stock Picker",
                "Priority": "default",
                "Tags": "chart_with_upwards_trend",
            },
            timeout=10,
        )

        response.raise_for_status()

        return (
            f"Push notification sent successfully via ntfy "
            f"(HTTP {response.status_code})"
        )

    except requests.RequestException as e:
        return f"Failed to send push notification via ntfy: {e}"