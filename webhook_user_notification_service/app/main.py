from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers import webhook_router, user_router

app = FastAPI()

CORS_SETTINGS = {
    "allow_origins": ["*"],  # Allow all origins
    "allow_credentials": True,
    "allow_methods": ["*"],  # Allow all HTTP methods
    "allow_headers": ["*"],  # Allow all headers
}

# Add CORS middleware to the application
app.add_middleware(CORSMiddleware, **CORS_SETTINGS)

app.include_router(webhook_router, tags=["webhook"])
app.include_router(user_router, tags=["user"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)