from fastapi import FastAPI, Depends
from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.routers import auth, organizations, users, notes
from app.services.auth import get_current_user
from scalar_fastapi import get_scalar_api_reference

app = FastAPI(title="Multi-Tenant Notes API", version="1.0.0")


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
app.include_router(users.router, prefix="/organizations/{org_id}/users", tags=["Users"])
app.include_router(notes.router, prefix="/notes", tags=["Notes"])

@app.get("/")
async def root():
    return {"message": "Multi-Tenant Notes API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/scalar")
async def scalar():
    return get_scalar_api_reference(
        title="Multi-Tenant Notes API",
        openapi_url=app.openapi_url
    )