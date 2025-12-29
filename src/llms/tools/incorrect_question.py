GEN_INCORRECT_WORD_QUESTION_TOOL = {
    "type": "function",
    "function": {
        "name": "gen_find_error_questions",
        "description": "Generate a list of 'Find the Error' English questions with indexed words.",
        "parameters": {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The erroneous sentence with indexed words. Example: 'He(1) go(2) to(3) school(4).'"
                            },
                            "choices": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of indexed words from the sentence to choose from."
                            },
                            "answer": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "The incorrect word(s) with index. Example: ['go(2)']"
                            },
                            "explanation": {
                                "type": "string",
                                "description": "The full CORRECT version of the sentence without indices. Example: 'He goes to school.'"
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Error types (e.g., 'verb tense', 'subject-verb agreement')."
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