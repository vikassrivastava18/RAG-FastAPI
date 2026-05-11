import asyncio, uuid
from langgraph.types import Command
from backend.core.agent.graph import build_graph
from backend.utils.utils import get_uuid_string
from dotenv import load_dotenv
from cachetools import TTLCache
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder

from backend.core.config import logger, Session, get_db
from backend.core.db.models import Chapter, Dialogue
from backend.core.db.query import get_content
from backend.core.db.schemas import (
    AnswerSchema,
    QuizRequest,
    ChapterInputRequest,
    UserQuery,
    NextTopicSchema
)

from backend.core.llm.generate import (
    chapter_summary,
    create_questions,
    create_quizzes,
    answer_query_util,
    generate_llm_response_quiz,
    evaluate,    
)

# Create Route instance
llm_routes = APIRouter()
# Load environment variables
load_dotenv()

cache = TTLCache(maxsize=1000, ttl=300)  # 5 minutes


@llm_routes.post("/chapter-summary")
def save_summary(request: ChapterInputRequest, db: Session = Depends(get_db)):
    # Fetch the first matching chapter
    chapter = db.query(Chapter).filter(Chapter.id == request.chapter_id).first()
    content = ""
    for subtopic in chapter.subtopics:
        content += subtopic.content + "\n"

    llm_summary = chapter_summary(content)
    return {
        "id": request.chapter_id,
        "name": chapter.chapter_name,
        "content": llm_summary,
    }


@llm_routes.post("/quiz-response/")
async def quiz_response(request: QuizRequest):
    try:
        # Retrieve the combined chunks for the user topics
        content = await get_content(request.selections)

        # Generate all Response for the the quiz types
        tasks = [
            generate_llm_response_quiz(
                content,
                q_type,
                number_of_question=request.number_of_question,
                language=request.language,
                notes=request.notes,
            )
            for q_type in request.question_types
        ]

        # Run all generate_case_study coroutines concurrently
        responses = await asyncio.tasks.gather(*tasks)

        res_data = "\n\n".join(responses)
        return {
            "topics": request.topics,
            "question_types": request.question_types,
            "data": res_data,
        }

    except Exception as e:
        logger.error("Error in quiz-response: %s", e)
        raise HTTPException(
            status_code=500, detail=f"Error processing the request: {str(e)}"
        )


@llm_routes.post("/generate-quizzes")
def generate_quizzes(request: ChapterInputRequest, db: Session = Depends(get_db)):
    # Fetch the first matching chapter
    chapter = db.query(Chapter).filter(Chapter.id == request.chapter_id).first()
    content = []

    for subtopic in chapter.subtopics:
        content.append({"url": subtopic.source, "content": subtopic.content})

    llm_quizzes = create_quizzes(content)
    return {"quizzes": llm_quizzes}


@llm_routes.post("/answer-query")
def answer_query(request: UserQuery):
    print("Request: ", request)
    docs = answer_query_util(request.query)
    return docs


@llm_routes.post("/generate-question")
def generate_questions(request: ChapterInputRequest, db: Session = Depends(get_db)):
    chapter = db.query(Chapter).filter(Chapter.id == request.chapter_id).first()
    content = []

    for subtopic in chapter.subtopics:
        content.append({"url": subtopic.source, "content": subtopic.content})

    llm_questions = create_questions(content)

    json_data = {
        "topic": llm_questions.questions[0].topic,
        "questions": jsonable_encoder(llm_questions.questions),
        "index": 0,
        "user_answer": "",
        "hint_taken": False,
        "llm_response": "",
        "state": "start",
    }

    # Create a new dialogue
    session_id = uuid.uuid4()
    dialogue = Dialogue(session_id=str(session_id), dialogue=json_data)
    db.add(dialogue)
    db.commit()

    json_data["session_id"] = str(session_id)
    return {"dialogue": json_data}


def prepare_data(
    session_id, data, index, user_answer, hint_taken, llm_resp, correct, state
):
    json_data = {
        "session_id": session_id,
        "topic": data.get("questions")[index].get("topic"),
        "question": data.get("questions")[index].get("question"),
        "index": index,
        "user_answer": user_answer,
        "hint_taken": hint_taken,
        "llm_response": llm_resp,
        "answer_correct": correct,
        "state": state,
    }
    return json_data


@llm_routes.post("/start-dialogue")
def start_dialogue(request: ChapterInputRequest, db: Session = Depends(get_db)):
    chapter = db.query(Chapter).filter(Chapter.id == request.chapter_id).first()

    topics = [
        {
            "url": subtopic.source,
            "content": subtopic.content,
            "topic": subtopic.subtopic_name,
            "notes": subtopic.content,
            "quizzes": [],
            "state": None,
            "messages": []
        }
        for subtopic in chapter.subtopics
    ]
    print("Subtopics length: ", len(topics))

    graph = build_graph()
    random_id = get_uuid_string()
    config = {"configurable": {"thread_id": random_id}}

    dialogues = {"index": -1, "dialogues": topics}

    result = graph.stream(dialogues, config)

    for chunk in result:
        if "__interrupt__" in chunk:                
            graph_query = chunk["__interrupt__"][0].value
            
            return {
                "dialogue": graph_query,
                "session_id": random_id
            }


@llm_routes.post("/review-response")
def review_response(request: AnswerSchema):
    session_id = request.session_id
    user_answer = request.answer
    print(session_id, user_answer)
    config = {"configurable": {"thread_id": session_id}}
    graph = build_graph()

    result = graph.stream(Command(resume=user_answer), 
                          config)
    graph_query = None
    state = None

    for chunk in result:
        if "__interrupt__" in chunk:                
            
            snapshot = graph.get_state(config).values
            state_index = snapshot["index"]
            state = snapshot["dialogues"][state_index]["state"]

            if state == "clear":
                graph_query = snapshot["dialogues"][state_index]["quizzes"] 
                graph_query = jsonable_encoder(graph_query)
            else:
                graph_query = chunk["__interrupt__"][0].value
            break

    if graph_query is None:
        return {
            "response": "The dialogue ends here.",
            "session_id": session_id,
            "state": state
        }

    return {
        "response": graph_query,
        "session_id": session_id,
        "state": state
    }
    
@llm_routes.post("/next-topic")
def next_topic(request: NextTopicSchema):
    session_id = request.session_id
    print("Session ID: ", session_id)
    config = {"configurable": {"thread_id": session_id}}
    graph = build_graph()

    result = graph.stream(Command(resume="Let's continue"), config)
    graph_query = None

    for chunk in result:
        if "__interrupt__" in chunk:
            graph_query = chunk["__interrupt__"][0].value
            break

    if graph_query is not None:
        return {
            "response": graph_query,
            "session_id": session_id
        }

    return {
        "response": "<p>The dialogue ends here.</p>",
        "session_id": session_id
    }     