from fastapi import FastAPI
from routers import auth, restore
from inference import Restore

app = FastAPI()

app.include_router(auth.router)
app.include_router(restore.router)

@app.on_event("startup")
async def subscribe_to_events():
    #initialize event subscriptions
    Restore()

@app.get("/")
def index():
    return "hello Walaalka!"
