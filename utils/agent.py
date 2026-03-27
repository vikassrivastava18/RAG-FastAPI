from typing import TypedDict

from core.config import llm2 as llm

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

def evaluate_answer(data):
    pass

def evaluate(data, hint=True) -> dict:
    """
    Evaluate the user reply, using LLM.
    Returns correct, retry or limits reached outputs
    """
    if not hint:
        ai_prompt = f"""
            You have to analyze the user's reply to a question to check the understanding of a concept and tell whether
            it is acceptable using notes provided to you.
            Return: correct or incorrect, along with some explanation. Also if answer is incorrect, give the correct answer based on notes
            in a friendly.
            Output sample 
            1) Correct: You have correctly understood use git branch in helping parallel feature development.
            2) Incorrect: Expected answer ...            
            Quiz: {data["question"]}
            Notes: {data["notes"]}
            User's reply: {data["users_answer"]}
        """
    else:
        ai_prompt = f"""
            You have to analyze the user's reply to a question to check the understanding of a concept and tell whether
            it is acceptable using notes provided to you.
            Return: correct or incorrect, along with some explanation. Also if answer is incorrect, give a hint to help user answer the question.
            Output sample
            1) Correct: You have correctly understood use git branch in helping parallel feature development.
            2) Incorrect: Here is a hint: ....
                            
            Quiz: {data["question"]}
            Notes: {data["notes"]}
            User's reply: {data["users_answer"]}
        """
    evaluation = llm.invoke(ai_prompt).content.lower()


    # print("Evaluation: ", evaluation)
    return {"role": "AI evaluation", "message": evaluation}
    

def dummy_evaluate():
    return  {
        "role": "AI evaluation",
        "message": "correct: your answer is correct!",
    }