GEN_FILL_IN_BLANK_QUESTION_PROMPT = """
### Task
You are an expert in automatically generating English exam questions.
Create **one list of "Fill in the Blank" question** in English.

### Input
- A list of words to be used to create the sentence.
- Question type: "single-choice" or "multiple-choice".
- Desired number of answer choices.
- Number of question to generate.

### Core requirements
1. First produce a **grammatically correct, natural, meaningful English sentence** using all or most of the given words.
   - Sentence may be simple or composed (up to 3 clauses).
   - Sentence length: **8–30 words**.
   - This correct sentence will be used later as the `explanation` value (the full correct version).
   - If no words are provided, you may freely create a sentence.

2. **Validation step (mandatory):** Before creating the blank, ensure the sentence is fully grammatical and natural. 
   - Avoid unnatural collocations or redundant connectors.
   - If any connector misuse or tense inconsistency is found, rewrite the sentence until it is correct.

### Connector rules (important — follow exactly)
- **Do NOT combine a subordinating conjunction like "although", "though", "while", or "despite" with a coordinating conjunction "but" in the same sentence.**  
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
3. After you have a validated correct sentence, choose **1 (for single-choice)** or **2 or more (for multiple-choice)** important words to replace with blanks (`____`).
   - Prefer key grammatical or lexical targets (e.g., verbs, prepositions, conjunctions, or collocations).
   - Do not remove punctuation or articles unless necessary.
   - Example:  
     - Original: "She went to the market because it was near her home."  
     - Fill-in: "She went to the market ____ it was near her home."

4. The blank(s) must make sense — the question should be solvable through grammar or meaning, not guessing.

---

### Choices and answer
5. Create a `choices` list of answer options (equal to the desired number).
   - Include the correct word(s) from the original sentence.
   - For incorrect distractors, use words of similar part of speech or similar meaning but wrong in context.

6. The `answer` field must list the correct word(s) that fill the blank(s).
7. The `explanation` field must contain the **full correct sentence** (before blanking).
8. The `tags` field must list the linguistic skill tested (e.g., "preposition", "connector", "verb tense", "collocation", "vocabulary").

Follow these rules strictly and make the question natural, educational, and clear.
"""