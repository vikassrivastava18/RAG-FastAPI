from pydantic import BaseModel

class MCQ(BaseModel):
    question: str
    options: list[str]
    answer: str
    explanation: str

class TrueFalse(BaseModel):
    question: str
    answer: bool
    explanation: str

class FillBlank(BaseModel):
    quiz: str
    answer: str

class QuizSchema(BaseModel):
    mcq: list[MCQ]
    true_false: list[TrueFalse]
    fill_blank: list[FillBlank]