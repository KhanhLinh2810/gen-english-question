GEN_FILL_IN_BLANK_QUESTION_PROMPT = """
### Task
You are an expert in automatically generating English exam questions.
Create **one list of "Fill in the Blank" questions** in English.

### Input
- A list of words to be used to create the sentence.
- Question type: "single-choice" or "multiple-choice".
- Desired number of answer choices.
- Number of questions to generate.

### Core requirements
1. First, produce a **grammatically correct, natural, and meaningful English sentence** using **some of the words** from the provided list.
   - The sentence may be simple or have **up to two clauses**.
   - Sentence length: **6–30 words**.
   - This correct sentence will later be used as the `explanation` value (the full correct version).
   - If no words are provided, you may freely create an appropriate sentence.

2. **Validation step (mandatory):** Before creating the blank, ensure the sentence is fully grammatical and natural.
   - Avoid unnatural collocations or redundant connectors.
   - If any connector misuse or tense inconsistency is found, rewrite the sentence until it is correct.

### Connector rules (important — follow exactly)
- **Do NOT combine a subordinating conjunction** such as "although", "though", "while", or "despite" **with a coordinating conjunction** like "but" in the same sentence.
  - Incorrect: "Although he was tired, but he continued."
  - Correct: "Although he was tired, he continued." or "He was tired, but he continued."
- Do NOT use duplicate connectors (e.g., "although ... however").
- Avoid redundant fillers such as "but yet", "and also", "and then then".
- If you use "because", do not also use "so" in the same causal relationship.

### IMPORTANT BALANCE RULE
- Do NOT overuse connectors.
- Prefer testing **verbs, verb tense, collocations, prepositions, vocabulary, or fixed expressions** when appropriate.
- Only test connectors when they are truly central to the sentence meaning.

---

### Blank-creation rules
3. After you have a validated correct sentence, choose:
   - **1 important word** for "single-choice", or
   - **2 or more important words** for "multiple-choice"
   to replace with blanks (`____`).
   - The version with blanks must be assigned to the `content` field.
   - The text replaced by blanks is the **answer** of the question.
   - Example:
     - content: "She ____ to bed later yesterday."
     - answer: ["went"]

4. The blank(s) must make sense — the question should be solvable through grammar or meaning, not guessing.

---

### Choices and answer
5. Create a `choices` list of answer options (equal to the desired number).
   - Include the correct answer.
   - For incorrect distractors:
     - Use words of the same part of speech or different forms/tenses of the same word.
     - If the answer is a verb, distractors must match the original tense or be plausible tense variants.
     - Distractors may be semantically similar but incorrect in context.

6. The `answer` field must list the correct word(s) that fill the blank(s).
7. The `explanation` field must contain the **full correct sentence** (before blanking).
8. The `tags` field must list the linguistic skill tested (e.g., "preposition", "connector", "verb tense", "collocation", "vocabulary").

Follow these rules strictly and make the question natural, educational, and clear.
"""
