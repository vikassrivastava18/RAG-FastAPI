import json

from dotenv import load_dotenv

from fastapi import (APIRouter, Request,
                     Depends, HTTPException,
                    status)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.config import Session, get_db, logger
from db.models import Book, Chapter, Subtopic
from db.schemas import (BookDetailFooterResponse,
                        BookDetailResponse,
                        ChapterRequest)

# Create Route instance
book_routes = APIRouter() 
# Load environment variables
load_dotenv()

# Configure the templates path
templates = Jinja2Templates(directory="frontend")

@book_routes.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "home_v2.html", {"request": request, "name": "FastAPI"}
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
        print(books)
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
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return book


@book_routes.post("/chapter-subtopics/", response_model=BookDetailResponse)
async def chapter_subtopics_list(request: ChapterRequest,
                                 db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == request.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return book


@book_routes.post("/add-book-new")
def add_book(file_path: str,
             db: Session = Depends(get_db)):
    try:
        # Open the file and load its content into a Python dictionary
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        new_book = Book(book_name=data["bookName"], book_file='...', logo1='folders/logos/logo.png')
        db.add(new_book) # Add record to session
        db.commit() # Commit transaction
        db.refresh(new_book) 

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

