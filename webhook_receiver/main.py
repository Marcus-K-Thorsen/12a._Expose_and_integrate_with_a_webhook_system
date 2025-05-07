from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict, List, Optional
from datetime import datetime, timezone

app = FastAPI()

CORS_SETTINGS = {
    "allow_origins": ["*"],  # Allow all origins
    "allow_credentials": True,
    "allow_methods": ["*"],  # Allow all HTTP methods
    "allow_headers": ["*"],  # Allow all headers
}

# Add CORS middleware to the application
app.add_middleware(CORSMiddleware, **CORS_SETTINGS)

# Set up templates for the frontend
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory database
received_events: List[Dict] = []  # To store all received webhook events

@app.post("/webhook")
async def webhook_endpoint(request: Request):
    """
    A simple webhook endpoint that logs the received payload and stores them in the in-memory database.
    """
    payload: Dict = await request.json()
    print(f"Received webhook payload: {payload}")
    
    event_type = payload.get("event_type", "unknown")
    event_data = payload.get("data", {})
    event = {
        "event_type": event_type,
        "data": event_data,
        "received_at": datetime.now(timezone.utc).isoformat()
    }
    received_events.append(event)
    
    print(f"Webhook received: {event}")
    
    return {"message": "Webhook received successfully"}


@app.get("/received-events", response_class=HTMLResponse)
async def show_received_events(
    request: Request, 
    event_filter: Optional[str] = Query(
        default=None, 
        description="Filter webhooks by specific event name (e.g., 'payment_received')."
    )):
    """
    Display the received webhook events in a simple UI.
    """
    filtered_events: List[Dict] = []
    if event_filter is not None:
        # Filter events based on the event_filter query parameter
        for received_event in received_events:
            if received_event["event_type"] == event_filter:
                filtered_events.append(received_event)
                
        return templates.TemplateResponse("index.html", {"request": request, "events": filtered_events})
    
    return templates.TemplateResponse("index.html", {"request": request, "events": received_events})



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)