def create_quizzes(content: ChapterContentRequest):
    prompt = f"""
    You are a quiz master. Use the content of a chapter to create quizzes that help students study.
    The content is divided into multiple subchapters, each with its source url and the text.
    You do not need to visit the url for a subchapter, but tag every quiz with its source url.
    Return the response in the format specified.    

    Content: {content}
    """

    structured_llm = llm2.with_structured_output(QuizResponse)
    messages = [
        {
            "role": "system",
            "content": prompt
        }
    ]

    response = structured_llm.invoke(messages)
    return response