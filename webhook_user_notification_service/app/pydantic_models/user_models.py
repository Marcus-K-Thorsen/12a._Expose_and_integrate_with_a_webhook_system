from pydantic import BaseModel, Field
from datetime import datetime, timezone

class SendMessageRequest(BaseModel):
    """
    Represents a request to send a message from one user to another.

    Attributes:
        sender (str): The username of the sender.
        recipient (str): The username of the recipient.
        subject (str): The subject of the message.
        message (str): The content of the message.
    """
    sender: str = Field(
        ...,
        description="The username of the sender.",
        example="bob"
    )
    recipient: str = Field(
        ...,
        description="The username of the recipient.",
        example="alice"
    )
    subject: str = Field(
        ...,
        description="The subject of the message.",
        example="Welcome!"
    )
    message: str = Field(
        ...,
        description="The content of the message.",
        example="Hi Alice, welcome to our service!"
    )


class SendMessageResponse(SendMessageRequest):
    """
    Represents the response after a message has been sent.

    Inherits all fields from SendMessageRequest and adds:
        received_at (str): The timestamp when the message was received.
    """
    received_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="The timestamp when the message was received.",
        example="2025-05-07T04:03:10.779082+00:00"
    )


class UserRequest(BaseModel):
    """
    Represents a request to register or interact with a user.

    Attributes:
        username (str): The username of the user.
    """
    username: str = Field(
        ...,
        description="The username of the user.",
        example="alice"
    )


class UserResponse(UserRequest):
    """
    Represents the response after a user has been registered or interacted with.

    Inherits all fields from UserRequest and adds:
        registered_at (str): The timestamp when the user was registered.
    """
    registered_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="The timestamp when the user was registered.",
        example="2025-05-07T04:03:10.779082+00:00"
    )