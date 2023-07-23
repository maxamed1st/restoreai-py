from dotenv import dotenv_values
from fastapi import FastAPI
from routers import auth, restore
from pymongo.mongo_client import MongoClient

app = FastAPI()

config = dotenv_values(".env")

@app.on_event("startup")
def startup_db_client():
    app.client = MongoClient(config["URI"])
    app.database = app.client[config["DB"]]
    app.collection = app.database[config["COL"]]

@app.on_event("shutdown")
def shutdown_db_client():
    app.client.close()

app.include_router(auth.router)
app.include_router(restore.router)

@app.get("/")
def index():
    return "hello Walaalka!"
