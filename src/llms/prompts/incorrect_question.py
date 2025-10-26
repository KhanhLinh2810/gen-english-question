GEN_INCORRECT_WORD_QUESTION_PROMPT = """
You are an expert English question generator.

### Task
Generate one "Find the Error" question in English.

### Input
- Words to use: {list_of_words}
- Question type: {question_type} ("single-choice" or "multiple-choice")
- Number of answer choices: {num_choices}

### Requirements
1. Create a natural English sentence using all or most of the given words.
2. The sentence can be **simple** (one clause) or **compound/complex** (two or more clauses joined by conjunctions like "and", "but", "when", "because", "although", etc.).
   - Choose whichever structure sounds most natural for the given words.
3. Introduce grammatical or vocabulary error(s):
   - If question_type = "single-choice": include exactly 1 incorrect word or phrase.
   - If question_type = "multiple-choice": include 2 or more incorrect words or phrases.
4. Mark each word in the sentence with an index number (e.g., "He(1) talk(2) when(3) I(4) talk(5).").
   - Each occurrence of a repeated word must have a unique index.
5. The `choices` must contain the **exact incorrect words or phrases** (no duplicates, no labels like A/B/C/D).
6. The `answer` must exactly match the incorrect word(s) with their indices.
7. Provide a corrected version of the sentence in `explanation`.
8. Include linguistic tags indicating the type of error (e.g., "verb tense", "article", "vocabulary", "subject-verb agreement", etc.).
9. Output must be **valid JSON only** in this format:

{
  "question": "He(1) talk(2) when(3) I(4) talk(5) because(6) he(7) angry(8).",
  "choices": ["talk(2)", "angry(8)", "because(6)", "he(7)"],
  "answer": ["talk(2)", "angry(8)"],
  "explanation": "He talks when I talk because he is angry.",
  "tags": ["verb tense", "adjective form"]
}

### Notes
- Ensure that the generated sentence sounds natural in English.
- You may use conjunctions or subordinate clauses when appropriate.
- Do not repeat the same word as two different answers.
- Output only the JSON object.
"""
