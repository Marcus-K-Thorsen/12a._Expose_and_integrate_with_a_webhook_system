import requests


exposee_base_url = "https://424e-85-82-70-165.ngrok-free.app"
integrator_base_url = "https://integrator-webhook.loca.lt"

# Subscribe the consumer server to webhook events
subscriptions = [
    {"event": "payment_received", "url": f"{integrator_base_url}/webhook"},
    {"event": "payment_processed", "url": f"{integrator_base_url}/webhook"},
    {"event": "invoice_processing", "url": f"{integrator_base_url}/webhook"},
    {"event": "invoice_completed", "url": f"{integrator_base_url}/webhook"}
]

def register_webhooks():
    for subscription in subscriptions:
        response = requests.post(f"{exposee_base_url}/register", json=subscription)
        if response.ok:  # Check if the response status code is 200-299
            print(f"Subscription response: {response.status_code}, {response.json()}")
        else:
            print(f"Failed to register webhook: {response.status_code}, {response.text}")



if __name__ == "__main__":
    register_webhooks()

