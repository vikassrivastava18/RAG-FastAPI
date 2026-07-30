from fastapi import APIRouter

from core.db.schemas import UserQuery
from utils.llm.generate import answer_query_util

ask_routes = APIRouter()


@ask_routes.post("/ask-query")
def ask_query(request: UserQuery):
    print("Request: ", request)
    docs = answer_query_util(request.query)
    return docs