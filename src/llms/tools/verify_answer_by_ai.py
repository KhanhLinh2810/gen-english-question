VERIFY_ANSWER_BY_AI_TOOL = {
    "type": "function",
    "function": {
        "name": "verify_ordering_questions",
        "description": (
            "Verify correct answers for English sentence-ordering "
            "multiple-choice questions."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "results": {
                    "type": "array",
                    "description": "Verification result for each question.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question_index": {
                                "type": "integer",
                                "description": "Question index (starting from 1)."
                            },
                            "correct_answer": {
                                "type": "string",
                                "description": (
                                    "Correct option label. Empty string if no valid answer."
                                ),
                                "enum": ["A", "B", "C", "D", "E", "F", "G", "H"]
                            },
                            "is_valid": {
                                "type": "boolean",
                                "description": (
                                    "True if exactly one correct answer exists, "
                                    "otherwise false."
                                )
                            },
                            "reason": {
                                "type": "string",
                                "description": (
                                    "Short justification explaining why the answer "
                                    "is correct or why the question is invalid."
                                )
                            }
                        },
                        "required": [
                            "question_index",
                            "correct_answer",
                            "is_valid",
                            "reason"
                        ]
                    }
                }
            },
            "required": ["results"]
        }
    }
}
