## Initial setup

```bash
$ poetry init -n
$ poetry add fastapi uvicorn requests
$ poetry shell
```


## How to run

```bash
$ cd webhook_user_notification_service\app
$ poetry run python main.py
```

Project will be running on http://127.0.0.1:8000

---

## Available Endpoints

### User Endpoints
- **POST** `/users`: Register a new user.
  - **Description**: This endpoint allows you to register a new user in the system. When this endpoint is called, it triggers the `user_registered` event. Any webhook registered to the `user_registered` event will receive a POST request with the relevant payload. This makes it possible for external systems to be notified whenever a new user is registered.

- **POST** `/users/messages`: Send a message from one user to another.
  - **Description**: This endpoint allows a user to send a message to another user. When this endpoint is called, it triggers the `user_send_message` event. Any webhook registered to the `user_send_message` event will receive a POST request with the relevant payload. This ensures that external systems can be notified whenever a message is sent between users.

- **GET** `/users/messages`: Retrieve all messages sent to a specific user.
  - **Description**: This endpoint retrieves all messages sent to a specific user. It does not trigger any webhooks.

- **GET** `/users`: Retrieve all registered users.
  - **Description**: This endpoint retrieves a list of all users currently registered in the system. It does not trigger any webhooks.

### Webhook Endpoints
- **POST** `/webhook`: Register a new webhook for a specific event.
- **DELETE** `/webhook`: Unregister a webhook for a specific event.
- **GET** `/webhooks`: Retrieve all registered webhooks grouped by event.
- **POST** `/ping`: Ping all registered webhooks or webhooks for a specific event to test their connectivity.

---

### How the User Endpoints Connect to the Webhook System

The `POST /users` and `POST /users/messages` endpoints are directly connected to the webhook system. When these endpoints are called:
1. The system checks for any webhooks registered to the corresponding event (`user_registered` or `user_send_message`).
2. If webhooks are registered, the system sends a POST request to each registered webhook URL with the event data as the payload.
3. This allows external systems to be notified in real-time whenever these events occur.

For example:
- If a webhook is registered to the `user_registered` event, it will be triggered whenever a new user is registered via the `POST /users` endpoint.
- If a webhook is registered to the `user_send_message` event, it will be triggered whenever a message is sent via the `POST /users/messages` endpoint.

This integration ensures that external systems can react to user-related events in the system without needing to constantly poll for updates.


---

For more details about each endpoint, including request and response formats, visit the Swagger documentation at:
**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## About `webhook_data.json`

The file [`webhook_data.json`](app/database_management/webhook_data.json) is used to store the registered webhook URLs for each event. It ensures that the system can persist webhook subscriptions between server restarts. 

You can find it in the following location:
**`webhook_user_notification_service/app/database_management/webhook_data.json`**

> **Note**: Be cautious when modifying this file directly, as it is managed by the system.