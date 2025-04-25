## Available Events
The following events are available for webhook registration:

1. **`user_registered`**: 
   - Triggered when a new user is registered. Useful for notifying external systems about new user signups.

2. **`user_send_message`**: 
   - Triggered when a user sends a message to another user. Useful for logging or notifying external systems about user interactions.

---

### How to Use These Events

1. **Register a Webhook**:
   - Use the `/webhook` endpoint to register a webhook for an event.
   - Example:
     ```bash
     curl -X POST "http://127.0.0.1:8000/webhook" \
     -H "Content-Type: application/json" \
     -d '{"event": "user_registered", "url": "http://your-webhook-receiver-url/webhook"}'
     ```

2. **Unregister a Webhook**:
   - Use the `/webhook` endpoint to remove a webhook for an event.
   - Example:
     ```bash
     curl -X DELETE "http://127.0.0.1:8000/webhook" \
     -H "Content-Type: application/json" \
     -d '{"event": "user_registered", "url": "http://your-webhook-receiver-url/webhook"}'
     ```

3. **Retrieve Registered Webhooks**:
   - Use the `/webhooks` endpoint to retrieve all registered webhooks grouped by event.
   - Example:
     ```bash
     curl -X GET "http://127.0.0.1:8000/webhooks"
     ```

4. **Ping Webhooks**:
   - Use the `/ping` endpoint to test all registered webhooks or webhooks for a specific event.
   - Example:
     ```bash
     curl -X POST "http://127.0.0.1:8000/ping" \
     -H "Content-Type: application/json"
     ```

---

## Available Endpoints

### User Endpoints
- **POST** `/users`: Register a new user and trigger webhooks for the `user_registered` event.
- **POST** `/users/messages`: Send a message from one user to another and trigger webhooks for the `user_send_message` event.
- **GET** `/users/messages`: Retrieve all messages sent to a specific user.
- **GET** `/users`: Retrieve all registered users.

### Webhook Endpoints
- **POST** `/webhook`: Register a new webhook for a specific event.
- **DELETE** `/webhook`: Unregister a webhook for a specific event.
- **GET** `/webhooks`: Retrieve all registered webhooks grouped by event.
- **POST** `/ping`: Ping all registered webhooks or webhooks for a specific event to test their connectivity.


### Ping Webhooks
The `/ping` endpoint allows you to test all registered webhooks or webhooks for a specific event. You can optionally provide a custom payload in the request body, which will be sent to the registered webhook URLs. If no payload is provided, a default payload will be used.

#### Notes
- If no payload is provided, the default payload will be:
  ```json
  {
    "message": "Ping from User Notification Webhook Service"
  }
  ```
- Replace `http://127.0.0.1:8000` with the server address provided by the webhook registration owner if the service is hosted elsewhere.

---

### Example Workflow

1. **Setup**:
   - The integrator sets up their webhook receiver at a URL of their choice (e.g., `http://your-webhook-receiver-url/webhook`).

2. **Register Webhooks**:
   - The integrator registers their webhook URL for the `user_registered` and `user_send_message` events.

3. **Test Webhooks**:
   - The integrator uses the `/ping` endpoint to verify that their webhook receiver is working correctly.
   - Optionally, the integrator can provide a custom payload to test specific scenarios.

4. **Send Events**:
   - The system triggers the `user_registered` event when a new user is registered and the `user_send_message` event when a user sends a message.

---

For more details about each endpoint, including request and response formats, visit the Swagger documentation at:
**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**