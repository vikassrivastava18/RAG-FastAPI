import uuid
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter

from core.config import Session, get_db, logger
from core.db.models import Chapter, Dialogue
from core.db.schemas import AnswerSchema, ChapterInputRequest

from utils.agent.graph import AnswerGraph
from utils.llm.generate import (
    create_questions,
    evaluate,
)

answer_routes = APIRouter()


@answer_routes.post("/start-dialogue")
def start_dialogue(request: ChapterInputRequest, db: Session = Depends(get_db)):
    try:
        chapter = db.query(Chapter).filter(Chapter.id == request.chapter_id).first()

        topics = [
            {"notes": subtopic.content, 
            "question": "", 
            "reply": "", 
            "hint_taken": False}
            for subtopic in chapter.subtopics[:3]
        ]

        graph = AnswerGraph.build_graph()
        random_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": random_id}}
        dialogues = {"topics": topics, "topic": {}}
        result = graph.stream(dialogues, config)

        for chunk in result:
            if "__interrupt__" in chunk:
                question = chunk["__interrupt__"][0].value

                return {
                        "dialogue": question,
                        "session_id": random_id
                        }
    except AttributeError as e:
        logger.error("Error in Fetching books: %s", e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Chapter not found"
            )

    except Exception as e:
        logger.error("Error occured: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Internal server error"
            )