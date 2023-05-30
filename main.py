from fastapi import FastAPI
from fastapi import HTTPException
from routes import contractors_router

app = FastAPI()

app.include_router(contractors_router)