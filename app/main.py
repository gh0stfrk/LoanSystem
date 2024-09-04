from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import user, loans



app = FastAPI(
    title="Loan Lender"
)
Base.metadata.create_all(engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_headers = ["*"],
    allow_methods = ["*"],
    allow_credentials = True
)

app.include_router(user.users)
app.include_router(loans.loans)

@app.get("/status")
async def status():
    return {
        "status": "OK",
    }