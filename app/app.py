from fastapi import FastAPI
from database.database import db, client
from database.database import check_mongo_connection
from app.auth import router as auth_router
from app.admin_events import router as admin_events_router
from middleware.isAdmin import AdminAuthMiddleware 
from app.admin_team import router as admin_team_router
from app.public_team import router as public_team_router
from app.public_events import router as public_events_router


app=FastAPI()

app.add_middleware(AdminAuthMiddleware)

@app.on_event("startup")
async def startup_event():
    await check_mongo_connection()

app.include_router(auth_router)
app.include_router(admin_events_router) 
app.include_router(admin_team_router)
app.include_router(public_team_router)
app.include_router(public_events_router)

@app.get("/test")
def test():
    return ({
        "message":"all good"
    })

@app.get("/admin/dashboard")
def dashboard():
    return {"message": "Welcome Admin!"}