## Webhook Receiver

This directory contains the **Webhook Receiver**, which is designed to simulate the role of an **Integrator** for testing purposes. It is intended to be used by the **Exposee** (the developer of the `webhook_user_notification_service`) to verify that webhooks are being sent correctly. 

This project is **not** meant to be used by the integrator who will be integrating the `webhook_user_notification_service` into their own system.

---

## Purpose

The Webhook Receiver provides a simple endpoint that listens for incoming webhook requests. It logs the payload received from the [Oliver exposee Webhook Project](https://github.com/OliverRoat/12a_Expose_and_integrate_with_a_webhook_system/tree/main/webhook).

The guide for the webhook exposee project can be found here: [**Webhook Integrator Guide**](https://github.com/OliverRoat/12a_Expose_and_integrate_with_a_webhook_system/blob/main/README.md).

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

### **GET** `/received-events`
- **Description**: This endpoint displays all received webhook events in a simple HTML table.
- **Behavior**:
  - Returns an HTML page (`webhook_receiver/templates/index.html`) that lists all received webhook events.
  - Allows filtering events by their `event_type` using the `event_filter` query parameter.
- **How to Use**:
  - Open the endpoint in a browser or make a GET request to `/received-events`.
  - To filter by a specific event type, append the `event_filter` query parameter to the URL. For example:
    - `/received-events?event_filter=payment_received` will show only events of type `payment_received`.
- **Example Response**:
  - The HTML page will display a table with the following columns:
    - **Event Type**: The type of the event (e.g., `payment_received`).
    - **Data**: The payload data received with the event.
    - **Received At**: The timestamp when the event was received.

---

## How to Start the Project

1. **Initial Setup**:
   Run the following commands to set up the project:
```bash
   $ poetry init -n
   $ poetry add fastapi uvicorn requests jinja2 python-multipart
   $ poetry shell
```

2. **Start the Webhook Receiver**:
   Run the following command to start the server:
```bash
   $ cd webhook_receiver
   $ poetry run python main.py
   $ lt --port 8001 --subdomain my-custom-subdomain
```

3. **Access the Webhook Receiver**:
   The Webhook Receiver will be running locally on `http://127.0.0.1:8001/webhook`.
   And it will be running on the internet on `https://my-custom-subdomain.loca.lt/webhook`

4. **Run the Webhook Script**:  
   Remember to have the exposee and integrator (webhook_receiver) running and set the `exposee_base_url` and the `integrator_base_url` to the correct urls.
   To start run the script use this command:
```bash
   $ cd webhook_receiver
   $ poetry run python webhook_script.py
```

