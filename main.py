from fastapi import FastAPI
from routers import auth, restore
from PubSub import EventHub
from inference import Restore

app = FastAPI()

app.include_router(auth.router)
app.include_router(restore.router)

@app.on_event("startup")
async def subscribe_to_events():
    #initialize EventHub
    EventHub()
    #initialize event subscriptions
    Restore()

@app.get("/")
def index():
    return "hello Walaalka!"
