import requests

WEBHOOK_URL = "https://example.com/webhook"  # mock


def trigger_alert(ticket, score):
    payload = {
        "message": f"High urgency ticket detected! Score: {score}",
        "ticket": ticket
    }

    print("Webhook Triggered:", payload)
    # requests.post(WEBHOOK_URL, json=payload)