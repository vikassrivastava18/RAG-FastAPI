import asyncio, uuid
from dotenv import load_dotenv
from cachetools import TTLCache
from sqlalchemy.orm.attributes import flag_modified
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder

from core.config import logger, Session, get_db
from db.models import Chapter, Dialogue
from db.query import get_content
from db.schemas import AnswerResponse, DialogueResponse, QuizRequest
from db.schemas import ChapterInputRequest, UserQuery

from llm.generate import (
    chapter_summary,
    create_questions,
    create_quizzes,
    answer_query_util,
    generate_llm_response_quiz,
    evaluate
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
        # topics = get_topics(request.selections)
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
    print("LLM response: ", llm_quizzes)
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
        "state": "start"
    }
    print("JSON data: ", json_data)
    session_id = uuid.uuid4()
    dialogue = Dialogue(session_id=str(session_id), dialogue=json_data)
    db.add(dialogue)
    db.commit()

    json_data["session_id"] = str(session_id)
    return {"dialogue": json_data}


def prepare_data(session_id, data, index, 
                 user_answer, hint_taken, llm_resp, correct, state):
    json_data = {
                "session_id": session_id,
                "topic": data.get("questions")[index].get("topic"),
                "question": data.get("questions")[index].get("question"),
                "index": index,
                "user_answer": user_answer,
                "hint_taken": hint_taken,
                "llm_response": llm_resp,
                "answer_correct": correct,
                "state": state
            }
    return json_data


@llm_routes.post("/evaluate-response")
def generate_dialogue(request: AnswerResponse, db: Session = Depends(get_db)):
    """
    1) Fetch the JSON blob using session_id, also the users answer.
    2) Review the user answer by invoking LLM call
    3) Update the Dialogue state based on correctness, in the database
    4) Return Dialogue response.
    """
    # 1
    session_id = request.session_id
    print(session_id)
    dialogue = db.query(Dialogue).filter(Dialogue.session_id == session_id).first()
    data = dialogue.dialogue
    index = data.get("index")
    question = data.get("questions")[index].get("question")
    ai_answer = data.get("questions")[index].get("answer")

    # Fetch the user's data 
    user_answer = request.answer
    # 2
    hint_available = False if data.get("hint_taken") else True
    evaluation = jsonable_encoder(evaluate(
        data={"question": question, "notes": ai_answer, "users_answer": user_answer},
        hint=hint_available,
    ))
    print("LLM evaluation: ", evaluation)
    answer_correct = evaluation["correct"] 
    llm_response = evaluation["comment"]
    data["user_answer"] = user_answer

    if answer_correct:
        data["index"] += 1
        data["hint_taken"] = False
        try:
            json_data = prepare_data(session_id, data, index+1,
                                     user_answer, False,
                                     llm_response, True, "correct")
            
        except IndexError:
            json_data = prepare_data(session_id, data, index,
                                     user_answer, False,
                                     llm_response, True, "END")

    else:
        data["answer_correct"] = False
        if hint_available:
            json_data = prepare_data(session_id, data, index,
                                     user_answer, False,
                                     llm_response, False, "hint")
            data["hint_taken"] = True
        else:
            try:
                json_data = prepare_data(session_id, data, index+1,
                                     user_answer, False,
                                     llm_response, False, "incorrect")
                
                data["index"] += 1
                data["hint_taken"] = False                
            except IndexError:
                json_data = prepare_data(session_id, data, index,
                                     user_answer, True,
                                     llm_response, False, "END")            
    # 3
    flag_modified(dialogue, "dialogue")
    db.commit()
    db.refresh(dialogue)
    # 4
    return {"dialogue": json_data}
