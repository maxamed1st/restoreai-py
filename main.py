from fastapi import FastAPI
from routers import auth, restore

app = FastAPI()

app.include_router(auth.router)
app.include_router(restore.router)

@app.get("/")
def index():
    return "hello Walaalka!"
