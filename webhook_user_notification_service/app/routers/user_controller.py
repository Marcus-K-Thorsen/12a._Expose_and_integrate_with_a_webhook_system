from fastapi import APIRouter, HTTPException, Query
from typing import List

from database_management import trigger_webhooks

from pydantic_models import (
    UserRequest,
    UserResponse,
    SendMessageRequest,
    SendMessageResponse
)

router: APIRouter = APIRouter()

# In-memory databases
send_message_store: List[SendMessageResponse] = []  # To store send messages
user_store: List[UserResponse] = []   # To store registered users


@router.post("/users", response_model=UserResponse)
async def register_user(user: UserRequest):
    """
    Register a new user and trigger webhooks for the 'user_registered' event.

    This endpoint allows the integrator to register a new user. Once registered, 
    the system triggers webhooks for the 'user_registered' event.

    Args:
        user (UserRequest): The user object containing the username to register.

    Returns:
        response (UserResponse): The registered user object, including the registration timestamp.

    Raises:
        HTTPException:
            - 400: If the username already exists.
    """
    # Check if the username is unique
    if any(existing_user.username.lower() == user.username.lower() for existing_user in user_store):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Register the user
    new_user = UserResponse(
        username=user.username.lower()
    )
    user_store.append(new_user)
    print(f"User registered: {new_user}")
    
    # Trigger webhooks for 'user_registered'
    trigger_webhooks("user_registered", new_user)
    
    return new_user



@router.post("/users/messages", response_model=SendMessageResponse)
async def send_message(send_message: SendMessageRequest):
    """
    Send a message and trigger webhooks for the 'user_send_message' event.

    This endpoint allows a user to send a message to another user. Once the message 
    is sent, the system triggers webhooks for the 'user_send_message' event.

    Args:
        send_message (SendMessageRequest): The message object containing the sender, recipient, subject, and message content.

    Returns:
        response (SendMessageResponse): The sent message object, including the timestamp.

    Raises:
        HTTPException:
            - 400: If the sender does not exist.
            - 400: If the recipient does not exist.
            - 400: If the sender and recipient are the same.
    """
    # Check if the sender exists
    if not any(user.username.lower() == send_message.sender.lower() for user in user_store):
        raise HTTPException(status_code=400, detail="Sender does not exist")
    # Check if the recipient exists
    if not any(user.username.lower() == send_message.recipient.lower() for user in user_store):
        raise HTTPException(status_code=400, detail="Recipient does not exist")
    # Check if the sender and recipient are different
    if send_message.sender.lower() == send_message.recipient.lower():
        raise HTTPException(status_code=400, detail="Sender and recipient cannot be the same")
    
    # Add metadata to the send message
    new_send_message = SendMessageResponse(
        sender=send_message.sender.lower(),
        recipient=send_message.recipient,
        subject=send_message.subject,
        message=send_message.message
    )
    send_message_store.append(new_send_message)
    print(f"Message sent: {new_send_message}")
    
    # Trigger webhooks for 'user_send_message'
    trigger_webhooks("user_send_message", new_send_message)
    
    return new_send_message

@router.get("/users/messages", response_model=List[SendMessageResponse])
async def get_send_messages(
    recipient: str = Query(
        default=...,
        description="The username of the recipient.",)
    ):
    """
    Retrieve sent messages for a specific user.

    This endpoint retrieves all messages sent to a specific user.

    Args:
        recipient (str): The username of the recipient.

    Returns:
        response (List[SendMessageResponse]): A list of messages sent to the specified recipient.

    Raises:
        HTTPException:
            - 400: If the recipient does not exist.
    """
    if not any(user.username == recipient.lower() for user in user_store):
            raise HTTPException(status_code=400, detail="Recipient does not exist")
    
    user_messages: List[SendMessageResponse] = []
    for message in send_message_store:
        if message.recipient.lower() == recipient.lower():
            user_messages.append(message)
    return user_messages

@router.get("/users", response_model=List[UserResponse])
async def get_users():
    """
    Retrieve all registered users.

    This endpoint retrieves a list of all users currently registered in the system.

    Returns:
        response (List[UserResponse]): A list of all registered users.
    """
    return user_store