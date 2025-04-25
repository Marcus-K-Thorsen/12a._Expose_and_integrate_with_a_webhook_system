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
- **POST** `/users/messages`: Send a message from one user to another.
- **GET** `/users/messages`: Retrieve all messages sent to a specific user.
- **GET** `/users`: Retrieve all registered users.

### Webhook Endpoints
- **POST** `/webhook`: Register a new webhook for a specific event.
- **DELETE** `/webhook`: Unregister a webhook for a specific event.
- **GET** `/webhooks`: Retrieve all registered webhooks grouped by event.
- **POST** `/ping`: Ping all registered webhooks or webhooks for a specific event to test their connectivity.

---

For more details about each endpoint, including request and response formats, visit the Swagger documentation at:
**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## About `webhook_data.json`

The file [`webhook_data.json`](app/database_management/webhook_data.json) is used to store the registered webhook URLs for each event. It ensures that the system can persist webhook subscriptions between server restarts. 

You can find it in the following location:
**`webhook_user_notification_service/app/database_management/webhook_data.json`**

> **Note**: Be cautious when modifying this file directly, as it is managed by the system.