GEN_FILL_IN_BLANK_QUESTION_TOOL = {
    "type": "function",
    "function": {
        "name": "gen_fill_in_blank_questions",
        "description": (
            "Generate a list of Fill in the Blank English questions based on the provided requirements."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "description": "A list of generated fill-in-the-blank questions.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The generated fill-in-the-blank sentence (e.g., 'She went to the market ____ it was near her home.')."
                            },
                            "choices": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of answer choices."
                            },
                            "answer": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of the correct answer word(s)."
                            },
                            "explanation": {
                                "type": "string",
                                "description": "The correct full version of the sentence (before creating blanks) and the reason why the answer is correct."
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of linguistic categories (e.g., 'connector', 'preposition')."
                            }
                        },
                        "required": ["content", "choices", "answer", "explanation", "tags"]
                    }
                }
            },
            "required": ["questions"]
        }
    }
}