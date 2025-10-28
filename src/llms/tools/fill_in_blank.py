GEN_FILL_IN_BLANK_QUESTION_TOOL = {
    "type": "function",
    "function": {
        "name": "gen_fill_in_blank_question",
        "description": (
            "Extract the components of a Fill in the Blank English question."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The generated fill-in-the-blank question (e.g., 'She went to the market ____ it was near her home.')."
                },
                "choices": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of answer choices (e.g., ['because', 'although', 'and', 'but'])."
                },
                "answer": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of the correct answer word(s) (e.g., ['because'])."
                },
                "explanation": {
                    "type": "string",
                    "description": "The correct full version of the sentence (before creating blanks)."
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of linguistic categories tested (e.g., 'connector', 'preposition', 'verb tense', etc.)."
                }
            },
            "required": ["question", "choices", "answer", "explanation", "tags"]
        }
    }
}
