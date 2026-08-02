import os
import sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import engine, Base
from core.db.models import (Book, 
                            Chapter, 
                            Subtopic, 
                            User, 
                            Dialogue)


Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()

# Include the home routers (loaded immediately)
from api.v1.books import book_routes
app.include_router(
    book_routes,
    tags=["Books"]
)

# Lazy load routers on demand
def load_auth_router():
    from api.v1.auth import auth_routes
    app.include_router(
        auth_routes,
        prefix="/auth",
        tags=["Authentication"]
    )

def load_ask_router():
    from api.v2.ask import ask_routes
    app.include_router(
        ask_routes,
        prefix="/ask",
        tags=["Ask"]
    )

def load_answer_router():
    from api.v2.answer import answer_routes
    app.include_router(
        answer_routes,
        prefix="/answer",
        tags=["Answer"]
    )

def load_dialogue_router():
    from api.v2.dialogue import dialogue_routes
    app.include_router(
        dialogue_routes,
        prefix="/dialogue",
        tags=["Dialogue"]
    )


def load_llm_router():
    from api.v1.llm import llm_routes
    app.include_router(
        llm_routes,
        prefix="/llm",
        tags=["LLM"]
    )

def load_admin_router():
    from api.v1.admin import admin_routes
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
    load_ask_router()
    load_answer_router()
    load_dialogue_router()
