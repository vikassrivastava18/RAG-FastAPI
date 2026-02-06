import json
import os
from core.utils import create_ppt_from_content
from db.query import get_content
from dotenv import load_dotenv

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from api.llm import cache
from core.config import Session, get_db, logger, get_current_user
from db.models import Book, Chapter, Subtopic
from db.schemas import (BookDetailFooterResponse, BookDetailResponse, 
                        ChapterRequest, PPTGenerationRequest, 
                        WorksheetRequestCompatible)
from llm.generate import generate_worksheet, get_ppt_content_from_llm

# Create Route instance
book_routes = APIRouter() 
# Load environment variables
load_dotenv()


# Configure the templates path
templates = Jinja2Templates(directory="frontend")


@book_routes.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "template.html", {"request": request, "name": "FastAPI"}
    )


@book_routes.get("/books")
def get_books(order: str = "asc", db: Session = Depends(get_db)):
    """Get books sorted by name asc/desc based on query param."""
    try:
        
        books = db.query(Book).filter(
            Book.book_name.isnot(None),
            Book.book_name != "",
            Book.status == True
        ).all()

        return [{
            "id": book.id, 
            "name": book.book_name
            } for book in books]
    except Exception as e:
        logger.error("Error in Case study: %s", e)
        raise HTTPException(status_code=500, detail=f"Error fetching sorted book list {e}")


@book_routes.get("/books/{book_id}/footer", response_model=BookDetailFooterResponse)
def get_book_footer(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    return book


@book_routes.delete("/books/{book_id}", response_model=dict)
async def delete_book(book_id: int, db: Session = Depends(get_db),
                      current_user: str = Depends(get_current_user)):
    """
    Delete a book and all its related chapters and subtopics.
    
    Parameters:
    - book_id: ID of the book to delete
    
    Returns:
    - {"status": "success", "message": "Book deleted successfully"} on success
    - Raises HTTPException with 404 if book not found
    - Raises HTTPException with 500 on other errors
    """
    try:       
        db.begin()
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            db.rollback()
            raise HTTPException(status_code=404, detail="Book not found")

        db.delete(book)
        db.commit()
        
        try:
            if book.book_file and os.path.exists(book.book_file):
                os.remove(book.book_file)
            if book.logo1 and os.path.exists(book.logo1):
                os.remove(book.logo1)
            if book.logo2 and os.path.exists(book.logo2):
                os.remove(book.logo2)
        except OSError as e:
            logger.error(f"Error deleting files for book {book_id}: {str(e)}")
   
        return {"status": "success", "message": "Book deleted successfully"}
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting book {book_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting the book: {str(e)}"
        )
 

@book_routes.post("/chapter-subtopics/", response_model=BookDetailResponse)
async def chapter_subtopics_list(request: ChapterRequest,
                                 db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == request.book_id).first()
    return book


@book_routes.get("/media/{file_path:path}")
async def get_media(file_path: str):
    response = FileResponse(file_path)
    response.headers["Cache-Control"] = "public, max-age=604800"  # 1 week
    return response


@book_routes.post("/generate-ppt/")
async def generate_ppt(request: PPTGenerationRequest, db: Session=Depends(get_db)):
    try:

        cache_key = f"{request.textbook_name}_{'_'.join(request.topics)}"
       
        all_slides = cache.get(cache_key)
        if not all_slides:
            combined_context = await get_content(request.selections)
            all_slides = await get_ppt_content_from_llm(
                context=combined_context, language=request.language, notes=request.notes
            )
        pptx_path = create_ppt_from_content(
            content=all_slides,
            textbook_name=request.textbook_name,
            book_id=request.book_id,
            db = db
        )

        filename = f"{request.textbook_name}.pptx"
        logger.warning(f"File name: {filename}, PPT path: {pptx_path}")
        return FileResponse(
            path=pptx_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )

    except Exception as e:
        logger.warning("Error in generation slide: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
        

# Worksheet API
@book_routes.post("/save-form/")
async def save_form(request: Request):
    try:
        data = await request.json()
        file_path = "user_data.json"

        if not os.path.exists(file_path):
            with open(file_path, "r+") as f:
                json.dump([], f)

        with open(file_path, "r+", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
            existing_data.append(data)

            f.seek(0)
            json.dump(existing_data, f, indent=4)
            f.truncate()
        return {"message": "Data saved successfully"}

    except Exception as e:
        logger.error("Error in saving user details: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": "An error occurred while saving data", "details": str(e)},
        )


@book_routes.post("/worksheet/")
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


@book_routes.post("/add-book-new")
def add_book(file_path: str,
             sub_chaps_same_page: bool = False,
             db: Session = Depends(get_db)
             ):
    try:
        # Open the file and load its content into a Python dictionary
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        new_book = Book(book_name=data["bookName"], book_file='...', logo1='folders/logos/logo.png')
        db.add(new_book) # Add record to session
        db.commit() # Commit transaction
        db.refresh(new_book) 

        # Add chapters and subtopics where subtopics are in the same page
        if sub_chaps_same_page:
            for chapter in data["chapters"]:
                # Add chapter
                new_chapter = Chapter(book_id=new_book.id, chapter_name=chapter["name"])
                db.add(new_chapter)
                db.commit()
                db.refresh(new_chapter)

                for i, subchapter in enumerate(chapter['subchapters']):
                    name = subchapter['name']
                    
                    try:
                        cont_start_ind = subchapter['content'].find(name)
                        next_sub_name = chapter['subchapters'][i+1]['name']            
                        cont_last_ind = subchapter['content'].find(next_sub_name)
                        subchapter['content'] =  subchapter['content'][cont_start_ind: cont_last_ind]
                    except IndexError:
                        subchapter['content'] = subchapter['content'][cont_start_ind:]

                    new_sub = Subtopic(chapter_id=new_chapter.id,
                                    subtopic_name=name,
                                    content=subchapter["content"][:4000])
                    db.add(new_sub)
                    db.commit()
                    db.refresh(new_sub)
        else:
        # Add chapters and subtopics
            for chapter in data["chapters"]:
                new_chapter = Chapter(book_id=new_book.id, chapter_name=chapter["name"])
                db.add(new_chapter)
                db.commit()
                db.refresh(new_chapter)

                # Store subchapters
                for subchapter in chapter["subchapters"]:
                    sub_name = subchapter["name"]
                    new_sub = Subtopic(chapter_id=new_chapter.id,
                                    subtopic_name=sub_name,
                                    content=subchapter["content"][:4000])
                    db.add(new_sub)
                    db.commit()
                    db.refresh(new_sub)

    except Exception as e:
        logger.error("Error in Adding new book: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))