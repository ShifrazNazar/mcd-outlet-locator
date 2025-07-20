from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import outlet_router, chatbot_router

app = FastAPI(
    title="McDonald's Outlet Locator API",
    description="API for finding McDonald's outlets with geospatial capabilities",
    version="1.0.0"
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(outlet_router)
app.include_router(chatbot_router)