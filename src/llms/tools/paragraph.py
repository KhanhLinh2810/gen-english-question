GEN_QUESTION_FOR_PARAGRAPH_OUTPUT_TOOL = {
    "type": "function",
    "function": {
        "name": "parse_paragraph_questions",
        "description": (
            "Parse the generated reading comprehension questions from a paragraph into structured JSON."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "list_questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The text of the generated single-choice question."
                            },
                            "choices": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of answer options."
                            },
                            "answer": {
                                "type": "string",
                                "description": "The correct answer."
                            }
                        },
                        "required": ["question", "choices", "answer"]
                    },
                    "description": "List of generated questions with choices and answers."
                }
            },
            "required": ["list_questions"]
        }
    }
}
