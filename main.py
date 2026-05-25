from fastapi import FastAPI
from api.routes import router

app=FastAPI(title="ScheduleMe")


app.include_router(router,prefix="/api/v1")

