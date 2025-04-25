from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook")
async def webhook_endpoint(request: Request):
    """
    A simple webhook endpoint that logs the received payload.
    """
    payload = await request.json()
    print(f"Received webhook payload: {payload}")
    return {"message": "Webhook received successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)