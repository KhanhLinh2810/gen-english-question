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
                "paragraph": {
                    "type": "string",
                    "description": "The English paragraph used to generate questions."
                },
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The text of the generated multiple-choice question."
                            },
                            "type": {
                                "type": "string",
                                "enum": ["FACT", "MAIN_IDEA", "VOCAB", "INFERENCE", "PURPOSE"],
                                "description": "The type of question."
                            },
                            "choices": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of answer options. Length must match `options_per_question`."
                            },
                            "answer": {
                                "type": "string",
                                "enum": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                                "description": "The correct answer (single character representing the choice)."
                            }
                        },
                        "required": ["question", "type", "choices", "answer"]
                    },
                    "description": "List of generated questions with choices and answers."
                }
            },
            "required": ["paragraph", "questions"]
        }
    }
}
