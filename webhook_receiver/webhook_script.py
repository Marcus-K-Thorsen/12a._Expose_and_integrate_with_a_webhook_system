import requests
from time import sleep


exposee_base_url = "http://127.0.0.1:8000"
integrator_base_url = "http://127.0.0.1:8001"

# Subscribe the consumer server to webhook events
subscriptions = [
    {"event_type": "payment_received", "url": f"{integrator_base_url}/webhook"},
    {"event_type": "payment_processed", "url": f"{integrator_base_url}/webhook"},
    {"event_type": "invoice_processing", "url": f"{integrator_base_url}/webhook"},
    {"event_type": "invoice_completed", "url": f"{integrator_base_url}/webhook"}
]

def register_webhooks():
    for subscription in subscriptions:
        response = requests.post(f"{exposee_base_url}/register", json=subscription)
        if response.ok:  # Check if the response status code is 200-299
            print(f"Subscription response: {response.status_code}, {response.json()}")
        else:
            print(f"Failed to register webhook: {response.status_code}, {response.text}")

def simulate_event(event_type: str):
    response = requests.post(f"{exposee_base_url}/simulate-event", json={"event_type": event_type})
    if response.ok:  # Check if the response status code is 200-299
        print(f"Simulate event response: {response.status_code}, {response.json()}")
    else:
        print(f"Failed to simulate event: {response.status_code}, {response.text}")

if __name__ == "__main__":
    # Register webhooks
    register_webhooks()

    # Simulate an event (example: payment_received)
    simulate_event("payment_received")
    sleep(1)  # Wait for a second
    simulate_event("payment_processed")
    sleep(2)  # Wait for two seconds
    simulate_event("invoice_processing")
    sleep(3)  # Wait for three seconds
    simulate_event("invoice_completed")
    sleep(1)  # Wait for a second
    simulate_event("payment_received")