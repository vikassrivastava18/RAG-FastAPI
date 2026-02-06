import asyncio
from dotenv import load_dotenv
from cachetools import TTLCache

from fastapi import (APIRouter,HTTPException)
from fastapi.responses import JSONResponse

from core.config import logger
from db.query import get_content
from llm.generate import (generate_llm_response_quiz, summarizer,
                          generate_case_study, get_ppt_content_from_llm,
                          generate_worksheet)                         
from db.schemas import (QuizRequest, SummarizeRequest, 
                        PPTPreviewRequest, CaseStudyRequest, 
                        WorksheetRequestCompatible
                        )

# Create Route instance
llm_routes = APIRouter() 
# Load environment variables
load_dotenv()

cache = TTLCache(maxsize=1000, ttl=300)  # 5 minutes


## content generation api
@llm_routes.post("/case-study/")
async def get_case_study_(request: CaseStudyRequest):
    try:
        content =  await get_content(request.selections)    
        # Create case study for all question types
        tasks = [
            generate_case_study(
                content,
                q_type,
                number_of_question=request.number_of_question,
                language=request.language,
                notes=request.notes,
            
            )for q_type in request.question_types
        ]

        # Run all generate_case_study coroutines concurrently
        case_studies = await asyncio.gather(*tasks)

        return {
            "topics": request.topics,
            "question_types": request.question_types,
            "data": case_studies,
        }

    except Exception as e:
        logger.error("Error in Case study: %s", e)
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


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


# End point for Summarize
@llm_routes.post("/summarize/")
async def summarize_text(request: SummarizeRequest):
    try:
        # topics = get_topics(request.selections)
        content = await get_content(request.selections)
        # Summarize the content using LLM
        summaries = await summarizer(content, request.language, request.notes)
        
        # Combine topic-summary pairs
        result = {
            "topic": [summaries]
        }
        return {"topics": request.topics, "data": result}

    except HTTPException as e:
        logger.error("Error in summarize: %s", e)
        raise e
    except Exception as e:
        logger.error("Error in summarize: %s", e)
        raise HTTPException(
            status_code=500, detail=f"Error processing the request: {str(e)}"
        )
    

# API for slide view
@llm_routes.post("/preview-slides/")
async def preview_slides(request: PPTPreviewRequest):
    try: 
        # Retrieve the combined chunks for the user topics
        # topics = get_topics(request.selections)
        combined_context = await get_content(request.selections)
        
        slides_data = await get_ppt_content_from_llm(
            context=combined_context,
            language=request.language,
            notes=request.notes,
        )
        cache_key = f"{request.textbook_name}_{'_'.join(request.topics)}"
        cache[cache_key] = slides_data
        return JSONResponse(content={"slides": slides_data, "cache_key": cache_key})

    except Exception as e:
        logger.error("Error in Preview slides: %s", e)
        raise HTTPException(
            status_code=500, detail=f"Error processing the request: {str(e)}"
        )


@llm_routes.post("/worksheet/")
async def get_worksheet(request: WorksheetRequestCompatible):
    try:
        # Retrieve the combined chunks for the user topics
        combined_context = await get_content(request.selections)

        # Generate one worksheet for all topics combined
        worksheet = generate_worksheet(
            question_type=request.question_types,
            number_of_question=request.number_of_question,
            language=request.language,
            notes=request.notes,
            context=combined_context,
        )

        return {
            "question_type": request.question_types,
            "number_of_question": request.number_of_question,
            "language": request.language,
            "notes": request.notes,
            "worksheet": worksheet,
        }

    except Exception as e:
        logger.error("Error in Worksheet: %s", str(e))
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )
