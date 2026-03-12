import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()
app.mount("/assets", StaticFiles(directory="frontend/assets"))


# Include the home routers (loaded immediately)
from api.books import book_routes
app.include_router(
    book_routes,
    tags=["Books"]
)


# Lazy load routers on demand
def load_auth_router():
    from api.auth import auth_routes
    app.include_router(
        auth_routes,
        prefix="/auth",
        tags=["Authentication"]
    )

def load_llm_router():
    from api.llm import llm_routes
    app.include_router(
        llm_routes,
        prefix="/llm",
        tags=["LLM"]
    )

def load_admin_router():
    from api.admin import admin_routes
    app.include_router(
        admin_routes,
        prefix="/admin",
        tags=["Admin"]
    )


# Load routers when app starts
@app.on_event("startup")
async def startup():
    load_auth_router()
    load_llm_router()
    load_admin_router()