DEFAULT_SYSTEM_PROMPT = """
    You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer
    the question. If you don't know the answer, say that you
    don't know. Use three sentences maximum and keep the
    answer concise.

    {context}

""".strip()

def generate_prompt(prompt: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
    return f"""
            [INST] <>
            {system_prompt}
            <>

            {prompt} [/INST]
        """.strip()