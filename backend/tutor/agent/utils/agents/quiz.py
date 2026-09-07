import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from typing import cast

from .schemas import QuizSchema


load_dotenv(override=True)

openai_key = os.getenv("OPENAI_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=SecretStr(openai_key) if openai_key else None,
    temperature=0.2,
    max_retries=2,
)


def create_quizzes(content: str) -> QuizSchema:
    prompt = f"""
    You are a quiz master. Use the content of a chapter to create quizzes that help students in their study.
    For MCQ, only one option should be correct.
    Return the response in the format specified.    

    Content: {content}
    """

    structured_llm = llm.with_structured_output(QuizSchema)
    messages = [
        {
            "role": "system",
            "content": prompt
        }
    ]

    response = structured_llm.invoke(messages)
    return cast(QuizSchema, response)