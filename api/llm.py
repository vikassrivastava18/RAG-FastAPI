import asyncio
from dotenv import load_dotenv
from cachetools import TTLCache

from fastapi import (APIRouter, HTTPException, Depends)

from core.config import logger, Session, get_db
from db.models import Chapter
from db.query import get_content
from llm.generate import (generate_llm_response_quiz)
from db.schemas import (QuizRequest
                        )

from db.schemas import (ChapterInputRequest,
                        UserQuery)

from llm.generate import (create_quizzes,
                          answer_query_util)

# Create Route instance
llm_routes = APIRouter() 
# Load environment variables
load_dotenv()

cache = TTLCache(maxsize=1000, ttl=300)  # 5 minutes


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
def generate_quizzes(request: ChapterInputRequest,
                     db: Session = Depends(get_db)):
    # Fetch the first matching chapter
    print("request", request)
    chapter = db.query(Chapter).filter(Chapter.id == request.chapter_id).first()
    content = []

    for subtopic in chapter.subtopics:
        content.append({"url": subtopic.source, "content": subtopic.content})

    llm_quizzes = create_quizzes(content)
    print("LLM response: ", llm_quizzes)
    return {
        "quizzes": llm_quizzes
    }


@llm_routes.post("/answer-query")
def answer_query(request: UserQuery):
    print("Request: ", request)
    docs = answer_query_util(request.query)

    return docs
