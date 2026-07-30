import uuid
from sqlalchemy.orm.attributes import flag_modified
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

from core.config import Session, get_db
from core.db.models import Chapter, Dialogue
from core.db.schemas import (
    AnswerSchema,
    ChapterInputRequest
)

from utils.llm.generate import (
    create_questions,
    evaluate,    
)

answer_routes = APIRouter()


def prepare_data(
    session_id, data, index, user_answer, 
    hint_taken, llm_resp, correct, state
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


@answer_routes.post("/generate-question")
def generate_question(request: ChapterInputRequest, db: Session = Depends(get_db)):
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


@answer_routes.post("/evaluate-response")
def generate_dialogue(request: AnswerSchema, db: Session = Depends(get_db)):
    """
        1) Fetch the JSON blob using session_id, also the users answer.
        2) Review the user answer by invoking LLM call
        3) Update the Dialogue state based on correctness, in the database
        4) Return Dialogue response.
    """
    # 1
    session_id = request.session_id
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
