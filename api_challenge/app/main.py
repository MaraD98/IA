from fastapi import FastAPI
from app.routers.endpoints import router


app = FastAPI()

# Incluye los endpoints definidos en endpoints.py
app.include_router(router)


