from typing import TypedDict

from core.config import llm2 as llm
from db.schemas import QueryResponse



def evaluate(data, hint=True) -> dict:
    """
    Evaluate the user reply, using LLM.
    Returns correct, retry or limits reached outputs
    """
    if not hint:
        ai_prompt = f"""
            You have to analyze the user's reply to a question to check the understanding of a concept and tell whether
            it is acceptable using notes provided to you.
            Return: 
                correct: True/False
                comment: comment on the answer, along with some explanation. Also if answer is incorrect, give the correct answer based on notes.
            in a friendly.          
            Quiz: {data["question"]}
            Notes: {data["notes"]}
            User's reply: {data["users_answer"]}
        """
    else:
        ai_prompt = f"""
            You have to analyze the user's reply to a question to check the understanding of a concept and tell whether
            it is acceptable using notes provided to you.
            Return: 
                correct: True/False
                comment: comment on the answer, along with some explanation. Also if answer is incorrect, make a comment on users answer and 
                give a hint to help user answer the question. Do not give the exact answer.
                            
            Quiz: {data["question"]}
            Notes: {data["notes"]}
            User's reply: {data["users_answer"]}
        """

    
    structured_llm = llm.with_structured_output(QueryResponse)
    messages = [
        {
            "role": "AI evaluation",
            "content": ai_prompt
        }
    ]

    response = structured_llm.invoke(messages)
    return response

def dummy_evaluate():
    import random
    r = random.random()
    correct = True if r > 0.5 else False
    return  {
        "correct": correct,
        "comment": "correct: your answer is correct!" if correct else "incorrect: ......",
    }