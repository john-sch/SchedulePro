from fastapi import FastAPI
from app.database import Base, engine
from app.routes.events import router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="SchedulePro API")
app.include_router(router, prefix="/events", tags=["events"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SchedulePro!"}
