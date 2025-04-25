## Webhook Receiver

This directory contains the **Webhook Receiver**, which is designed to simulate the role of an **Integrator** for testing purposes. It is intended to be used by the **Exposee** (the developer of the `webhook_user_notification_service`) to verify that webhooks are being sent correctly. 

This project is **not** meant to be used by the integrator who will be integrating the `webhook_user_notification_service` into their own system.

---

## Purpose

The Webhook Receiver provides a simple endpoint that listens for incoming webhook requests. It logs the payload received from the `webhook_user_notification_service` to verify that the webhooks are functioning as expected.

---

## Available Endpoint

### **POST** `/webhook`
- **Description**: This endpoint receives webhook payloads sent by the `webhook_user_notification_service`.
- **Behavior**: 
  - Logs the received payload to the console.
  - Responds with a success message to confirm receipt of the webhook.
- **Example Response**:
  ```json
  {
    "message": "Webhook received successfully"
  }
  ```

---

## How to Start the Project

1. **Initial Setup**:
   Run the following commands to set up the project:
   ```bash
   $ poetry init -n
   $ poetry add fastapi uvicorn
   $ poetry shell
   ```

2. **Start the Webhook Receiver**:
   Run the following command to start the server:
   ```bash
   $ poetry run uvicorn main:app --host 127.0.0.1 --port 8001 --reload
   ```

3. **Access the Webhook Receiver**:
   The Webhook Receiver will be running on `http://127.0.0.1:8001/webhook`.

