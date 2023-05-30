from fastapi import FastAPI
from fastapi import HTTPException
from routes import contractors_router, contractors_router_db

app = FastAPI()

app.include_router(contractors_router)
app.include_router(contractors_router_db)