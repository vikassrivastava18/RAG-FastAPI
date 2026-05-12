from fastapi import APIRouter

from backend.core.db.schemas import UserQuery
from backend.core.llm.generate import answer_query_util

ask_routes = APIRouter()


@ask_routes.post("/ask-query")
def ask_query(request: UserQuery):
    print("Request: ", request)
    docs = answer_query_util(request.query)
    return docs