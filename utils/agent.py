from typing import TypedDict

class QuizSate(TypedDict):
    topic: str
    notes: str
    question: str
    messages: list
    attempts: int

class DialoguesState(TypedDict):
    index: int
    topics: list
    messages: list
    all_messages: list
    quiz: QuizSate


def setup_dailogue(chapter_id: int):
    chapter = db.query(Chapter).filter(Chapter.id == request.chapter_id).first()
    content = []

def update_dialogue():
    pass

def evaluate_answer():
    pass