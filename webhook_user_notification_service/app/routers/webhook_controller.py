from fastapi import APIRouter, HTTPException, Query, Body, status
from typing import Optional, List, Dict, Any

from database_management import (
    update, 
    remove, 
    read,
    send,
    WebhookEventNotFoundError,
    WebhookEventHasNoURLsError,
    WebhookUrlNotFoundError,
    WebhookUrlAlreadyExistsError
    )

from pydantic_models import (
    WebhookResponse, 
    WebhookRequest,
    Webhook,
    RegisteredWebhooksResponse,
    PingResponse
)

router: APIRouter = APIRouter()



@router.post("/webhook", response_model=WebhookResponse)
def register_webhook(webhook: WebhookRequest):
    """
    Register a new webhook for a specific event.

    This endpoint allows the integrator to register a webhook URL for a specific event. 
    The webhook will be triggered whenever the specified event occurs.

    Args:
        webhook (WebhookRequest): The webhook object containing the event name and URL.

    Returns:
        response (WebhookResponse): A success message indicating that the webhook was registered, 
        along with the event name and URL.

    Raises:
        HTTPException: 
            - 404: If the specified event does not exist.
            - 400: If the URL is already registered for the given event.
    """
    try:
        update(webhook.event, str(webhook.url))
        return WebhookResponse(
            message="Webhook registered successfully",
            url=webhook.url,
            event=webhook.event
        )
        
    except WebhookEventNotFoundError:
        raise HTTPException(status_code=404, detail=f"Event '{webhook.event}' not found")
    except WebhookUrlAlreadyExistsError:
        raise HTTPException(status_code=400, detail=f"Webhook URL '{webhook.url}' already exists for event '{webhook.event}'")
    

@router.delete("/webhook", status_code=status.HTTP_204_NO_CONTENT)
def unregister_webhook(webhook: WebhookRequest):
    """
    Unregister a webhook for a specific event.

    This endpoint allows the integrator to remove a previously registered webhook URL 
    for a specific event. Once unregistered, the webhook will no longer be triggered 
    for the specified event.

    Args:
        webhook (WebhookRequest): The webhook object containing the event name and URL.

    Returns:
        response (None): Returns a 204 No Content status code on successful deletion.

    Raises:
        HTTPException: 
            - 404: If the specified event does not exist.
            - 404: If the URL is not registered for the given event.
    """
    try:
        return remove(webhook.event, str(webhook.url))
        
    except WebhookEventNotFoundError:
        raise HTTPException(status_code=404, detail=f"Event '{webhook.event}' not found")
    except WebhookUrlNotFoundError:
        raise HTTPException(status_code=404, detail=f"Webhook URL '{webhook.url}' not found for event '{webhook.event}'")


@router.get("/webhooks", response_model=RegisteredWebhooksResponse)
def get_all_registered_webhooks(
    event_filter: Optional[str] = Query(
        default=None, 
        description="Filter webhooks to return by a specific event name (e.g., 'user_registered')."
    )
):
    """
    Retrieve all registered webhooks grouped by event.

    This endpoint returns a list of all registered webhooks grouped by event. 
    If an event filter is provided, only the webhooks for that specific event are returned.

    Args:
        event_filter (str | None): The event name to filter webhooks. If None, all events are returned.

    Returns:
        response (RegisteredWebhooksResponse): A dictionary where the keys are event names and the values 
        are lists of webhook URLs.

    Raises:
        HTTPException: 
            - 404: If the specified event does not exist.
            - 404: If the specified event exists but has no registered URLs.
    """
    try:
        # Read all registered webhooks from storage
        data = read(event_filter)

        webhooks: List[Webhook] = []
        
        for webhook_event, webhook_urls in data.items():
            # Create a Webhook object for each event and its URLs
            webhook = Webhook(
                event=webhook_event,
                urls=webhook_urls
            )
            webhooks.append(webhook)
            

        return RegisteredWebhooksResponse(webhooks=webhooks)
    
    except WebhookEventNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail=f"Event '{event_filter}' not found."
        )
    except WebhookEventHasNoURLsError:
        raise HTTPException(
            status_code=404, 
            detail=f"Event '{event_filter}' has no registered URLs."
        )

@router.post("/ping", response_model=PingResponse)
def ping_all_webhooks(
    event_filter: Optional[str] = Query(
        default=None, 
        description="Filter webhooks to ping by specific event name (e.g., 'user_registered')."
    ),
    payload: Optional[Dict[str, Any]] = Body(
        default=None,
        description="Optional payload to send to the webhooks. If not provided, a default payload will be used.",
        example={
            "test_key": "test_value",
            "message": "This is a test payload for webhook testing."
        }
    )
):
    """
    Ping all registered webhooks across all events or for a specific event.

    This endpoint sends a test payload to all registered webhooks for all events or a specific event.
    It provides a summary of successful and failed webhook calls.

    Args:
        event_filter (str | None): The event name to filter webhooks. If None, all events are pinged.
        payload (dict | None): An optional payload to send to the webhooks. If not provided, a default payload is used.

    Returns:
        response (PingResponse): A summary of the ping operation, including the number of successful and failed webhooks.

    Raises:
        HTTPException: 
            - 404: If no webhooks are registered for a queried event.
            - 404: If the specified event exists but has no registered URLs.
    """
    try:
        # Read webhooks from storage
        data = read(event_filter)

        # Use the provided payload or fall back to the default payload
        payload_to_send = payload or {"message": "Ping from User Notification Webhook Service"}

        # Send pings to the webhooks
        pinged_webhooks = send(data, payload_to_send)

        # Construct the response message
        message = (
            "Pinged all registered webhooks successfully."
            if event_filter is None
            else f"Pinged webhooks for event '{event_filter}' successfully."
        )

        # Return the PingResponse
        return PingResponse(
            message=message,
            **pinged_webhooks.model_dump()
        )

    except WebhookEventNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail=f"Event '{event_filter}' not found."
        )
    except WebhookEventHasNoURLsError:
        raise HTTPException(
            status_code=404, 
            detail=f"Event '{event_filter}' has no registered URLs."
        )