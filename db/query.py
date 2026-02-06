from typing import List

from core.config import Session, logger
from core.utils import verify_password
from db.schemas import ChapterCreate
from .models import Chapter, Subtopic, User


async def get_content(selections: List[dict]):
    db = Session()
    result = []
    for selection in selections:
        # Fetch the first matching chapter
        chapter = db.query(Chapter).filter(Chapter.chapter_name == selection["chapter"]).first()
        # Ensure chapter exists (to avoid NoneType errors)
        if chapter:
            # Use the chapter_id in the Subtopic query
            subtopics = db.query(Subtopic).filter(Subtopic.chapter_id == chapter.id).all()
            result.extend(subtopics)
    data = [subtopic.content for subtopic in result]
    data = "\n\n".join(data)
    return data


def bulk_insert_chapters(data: List[ChapterCreate], book_id: int, db: Session):
    for chapter_data in data:
        # print("Raw chapter data:", chapter_data)  
        if not isinstance(chapter_data, dict):
            logger.error(f"Invalid chapter data format: {type(chapter_data)}")
            continue
            
        try:
            chapter = Chapter(
                chapter_name=chapter_data.get('chapter_title'),
                book_id=book_id
            )
            db.add(chapter)
            db.flush()

            subtopics = chapter_data.get("subtopics", [])
            if not isinstance(subtopics, list):
                logger.error(f"Invalid subtopics format: {type(subtopics)}")
                continue
                
            for subtopic_title in subtopics:
                sub = Subtopic(subtopic_name=subtopic_title, chapter_id=chapter.id)
                db.add(sub)
                
        except Exception as ex:
            logger.error(f"Error processing chapter: {ex}", exc_info=True)
            db.rollback()
            raise  # Re-raise after logging
    
    try:
        db.commit()
    except Exception as error:
        logger.error(f"Commit error: {error}", exc_info=True)
        db.rollback()
        raise


def authenticate_user(username, password):
    db = Session()
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return None

    # Verify password
    if verify_password(password, user.password):
        return user

