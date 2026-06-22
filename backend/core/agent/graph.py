from dotenv import load_dotenv

from typing import Literal
from pydantic import BaseModel
from langchain_core.messages import (AIMessage,
                                     HumanMessage,
                                     SystemMessage)

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt

from core.config import llm
from core.agent.schemas import DialogueState, QuizSchema


load_dotenv(override=True)
checkpointer = InMemorySaver()

def set_topic_index(state: DialogueState) -> DialogueState:
    state["index"] += 1
    return state


def remaining(state: DialogueState) -> Literal["remaining", "complete"]:
    next_index = state["index"]

    if next_index >= len(state["dialogues"]):
        return "complete"
    return "remaining"


def concept_summary(state: DialogueState) -> DialogueState:
    """LLM should prepare a friendly summary on the topic."""
    
    context = "\n".join([topic["notes"] for topic in state["dialogues"]])    
    concept_prompt = f"""
    Prepare a summary on the topic. Use notes for preparing summary and
    context information as overall context while preparing the conceptual summary.
    Wrap the output in HTML tags like <p>, <i>, but do not introduce unnecessary header tags like
    <header>, <html>, <body>.

    Topic: {state["dialogues"][state["index"]]["topic"]}
    Notes: {state["dialogues"][state["index"]]["notes"]}
    Context: {context}

    End the output with something like "Any doubts?".
    Output Sample (Follow format strictly!!): 
        <b>Topic</b>  <p>How to get rich in 100 days?</p> <p>There are many ways, best
        path is to work hard....</p>
    """
    summary = llm.invoke(concept_prompt).content
    
    state["dialogues"][state["index"]]["messages"].append(AIMessage(content=summary))
    return state


def get_user_reply(state: DialogueState) -> DialogueState:
    summary = state["dialogues"][state["index"]]["messages"][-1].content
    user_reply = interrupt(
        f"{summary}" 
    )
    state["dialogues"][state["index"]]["messages"].append(HumanMessage(content=user_reply))
    return state


class IntentSchema(BaseModel):
    intent: Literal["hint", "clear"]


def reply_intent(state: DialogueState) -> Literal["hint", "clear"]:
    
    user_reply = (
        state["dialogues"][state["index"]]["messages"][-1].content
    )

    intent_prompt = f"""
    Look at the user's latest reply and determine the intent.

    Return:
    - "hint" -> if the user is confused or wants more clarity
    - "clear" -> if the user understands the concept

    User Reply:
    {user_reply}
    """

    structured_llm = llm.with_structured_output(IntentSchema)
    response = structured_llm.invoke(intent_prompt)
    state["dialogues"][state["index"]]["state"] = response.intent
    return response.intent


def clarify_doubt(state: DialogueState) -> DialogueState:
    clarify_prompt = f"""Look at the past converstaion on a topic and latest user's reply to clarify user's doubts.
    Output format:  <p>There are many ways, best
    path is to work hard....</p>
    """
    system_message = AIMessage(content=clarify_prompt)
    messages = [system_message] + state["dialogues"][state["index"]]["messages"]
    
    response = llm.invoke(messages).content
    state["dialogues"][state["index"]]["messages"].append(AIMessage(content=response))

    return state


def prepare_quiz(state: DialogueState) -> DialogueState:
    
    content = state["dialogues"][state["index"]]["notes"]
    prompt = f"""
    You are a quiz master. Use the content of a topic to create questions (MCQ's and True/False) and expected answers 
    that help students in their study.
    Return the response in the format specified.    
    
    Content: {content}
    """

    structured_llm = llm.with_structured_output(QuizSchema)
    messages = [SystemMessage(content=prompt)]
    
    quizzes = structured_llm.invoke(messages)
    
    state["dialogues"][state["index"]]["quizzes"] = quizzes

    return state
    

def quiz_response(state: DialogueState) -> DialogueState:
    quizzes = state["dialogues"][state["index"]]["quizzes"]
    # Get user's reply to quiz
    user_reply = interrupt(
        f"{quizzes}"
    )
    return state


def build_graph():
    builder = StateGraph(DialogueState)

    builder.add_node("set_topic_index", set_topic_index)
    builder.add_node("concept_summary", concept_summary)
    builder.add_node("get_user_reply", get_user_reply)
    builder.add_node("clarify_doubt", clarify_doubt)
    builder.add_node("prepare_quiz", prepare_quiz)
    builder.add_node("quiz_response", quiz_response)

    builder.set_entry_point("set_topic_index")
    builder.add_conditional_edges(
        "set_topic_index",
        remaining,
        {
            "remaining": "concept_summary",
            "complete": END
        }
    )
    builder.add_edge("concept_summary", "get_user_reply")
    builder.add_conditional_edges(
        "get_user_reply",
        reply_intent,
        {
            "hint": "clarify_doubt",
            "clear": "prepare_quiz"
        }
    )
    builder.add_edge("clarify_doubt", "get_user_reply")
    builder.add_edge("prepare_quiz", "quiz_response")
    builder.add_edge("quiz_response", "set_topic_index")

    return builder.compile(checkpointer)

