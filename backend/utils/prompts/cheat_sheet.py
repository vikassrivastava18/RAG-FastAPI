
def cheat_prompt(content):
    Cheat_prompt = """
    Create a cheat-sheet summary of the conents of a chapter. Divide the chapter into topics. Keep it around 400 words. Along
    with summary, generate some valid code snippets for the topics.
    For every snippet, output only valid Python source code. The snippet must be syntactically valid Python 3 and must 
    compile successfully when passed to Python's compile() with mode "exec". Do not use pseudocode, placeholders, ellipses 
    (...), or explanatory text inside the snippet. Do not wrap the snippet in Markdown code fences.

    Content: {content}
    """
    

