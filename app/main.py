from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.routes.events import router

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SchedulePro API")
app.include_router(router, prefix="/events", tags=["events"])

# Mount the React build directory at /dashboard
app.mount("/dashboard", StaticFiles(directory="frontend/build", html=True), name="dashboard")

@app.get("/")
def read_root():
    return {"message": "Welcome to SchedulePro API!"}
