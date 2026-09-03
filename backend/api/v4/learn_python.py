from fastapi import APIRouter
from config import llm2
from core.db.schemas import TopicRequest, TopicsCheatSheetResponse
from utils.prompts.cheat_sheet import cheat_prompt

python_routes = APIRouter()

@python_routes.post("/create-cheatsheet")
def create_cheatsheet(request: TopicRequest):
    global cheat_prompt
    cheat_prompt = cheat_prompt(request.content)
    resp = llm2.with_structured_output(TopicsCheatSheetResponse)
    print(resp.content)
    return resp.content
    
    

@python_routes.post("create-codes")
def create_code(request):
    pass