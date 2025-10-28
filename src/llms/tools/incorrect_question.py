GEN_INCORRECT_WORD_QUESTION_TOOL = {
    "type": "function",
    "function": {
        "name": "gen_find_error_question",
        "description": (
            "Extract infomations of question."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The generated question: an erroneous English sentence with each word indexed (e.g., 'He(1) talk(2) when(3) I(4) talk(5).')."
                },
                "choices": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of answer choices. Each choice is an indexed word/phrase from the question (e.g., 'talk(2)')."
                },
                "answer": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of the *exact* incorrect word(s)/phrase(s) *with their indices* (e.g., ['talk(2)', 'angry(8)']). This must match the incorrect options in 'choices'."
                },
                "explanation": {
                    "type": "string",
                    "description": "The grammatically correct version of the sentence (the original sentence from step 1 of the prompt), without indices."
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of linguistic error types introduced in the question (e.g., 'verb tense', 'article', 'vocabulary')."
                }
            },
            "required": ["question", "choices", "answer", "explanation", "tags"]
        }
    }
}