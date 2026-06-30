from .llm import chat_json

def score_answer(question: dict, answer: str) -> dict:
    """Evaluates the candidate's response against rubric constraints using LLM judgment."""
    system = (
        "You are an expert technical interviewer and executive communication coach. "
        "Score the candidate's answer from 1 to 10 based on clarity, technical relevance, and core structure. "
        "For behavioral responses, assess adherence to the STAR framework. For technical options, assess accuracy. "
        "Return a JSON object matching this exact shape: "
        '{"clarity": int, "relevance": int, "structure": int, "overall": int, '
        '"strengths": ["string"], "improvements": ["string"], "rewritten_answer": "string"}'
    )
    user = (
        f"Question Context ({question['type'].upper()} - Domain: {question['competency']}):\n"
        f"Prompt: {question['text']}\n\n"
        f"Candidate Provided Answer:\n{answer}"
    )
    return chat_json(system, user)