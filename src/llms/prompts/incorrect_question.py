GEN_INCORRECT_WORD_QUESTION_PROMPT = """
### Task
You are an expert in automatically generating English exam questions.
Create **one list of "Find the Error" questions** in English.

### Input
- A list of words to be used to create the sentence.
- Question type: "single-choice" or "multiple-choice".
- Desired number of answer choices.
- Number of questions to generate.

### Core requirements
1. First, produce a **grammatically correct, natural, and meaningful English sentence**
   using **some of the words** from the provided list.
   - The sentence may be simple or have **up to two clauses**.
   - Sentence length: **6–30 words**.
   - This correct sentence will later be used as the `explanation` value
     (the full correct version).
   - If no words are provided, you may freely create an appropriate sentence.

2. **Validation step (mandatory):**
   Before introducing any errors, ensure the sentence is fully grammatical and natural.
   - Avoid unnatural collocations or redundant connectors.
   - If any connector misuse or tense inconsistency is found,
     rewrite the sentence until it is correct.

### Semantic coherence rule (mandatory)
- All clauses in the sentence must describe actions or states that belong to
  the SAME situation, routine, purpose, or cause–effect context.
- Do NOT combine unrelated activities, abstract decisions,
  or different time frames in one sentence.
- If the sentence contains multiple verbs, they must describe
  the same routine, one process, or a clear cause–effect relationship.

### Connector rules (important — follow exactly)
- **Do NOT combine a subordinating conjunction**
  such as "although", "though", "while", or "despite"
  **with a coordinating conjunction** like "but" in the same sentence.
  - Incorrect: "Although he was tired, but he continued."
  - Correct: "Although he was tired, he continued."
    or "He was tired, but he continued."
- Do NOT use duplicate connectors (e.g., "although ... however").
- Avoid redundant fillers such as "but yet", "and also", "and then then".
- If you use "because", do not also use "so" in the same causal relationship.

### Error-introduction rules
3. After you have a validated correct sentence, create an **erroneous version**
   by introducing errors according to `question_type`:
   - `single-choice`: introduce **exactly 1 error**.
   - `multiple-choice`: introduce **2 or more errors**.
   - **The erroneous sentence MUST be different from
     the original correct sentence.**
   - **At least one word or phrase must be changed
     (added, removed, or replaced)
     so that the sentence becomes grammatically incorrect or unnatural.**
   - The introduced error must be a **CLEAR grammatical or lexical error**;
     do NOT rely on vague unnaturalness or debatable usage.

4. **Self-check (mandatory):**
   Compare the erroneous sentence with the correct sentence.
   - If they are identical or differ only in punctuation,
     rewrite the erroneous sentence until a real error is introduced.

- The erroneous version must be assigned to the `content` field.
   - The correct text replaced by errors is the **answer** of the question.
   - Example:
     - content: "She go to bed late yesterday."
     - answer: ["go"]
     - explanation: "She went to bed late yesterday."

5. Add an index number to each word in the erroneous sentence
   (e.g., "He(1) work(2) when(3) I(4) sleep(5).").

### Choices and answer
6. Create a `choices` list
   (each option must include the index number as shown in the sentence).
   - Include the correct answer.
   - For incorrect distractors:
     - Each option must be a **word or short phrase**
       extracted from the erroneous sentence.
     - Each option must include both the **text**
       and its **index/indices** in the sentence.

7. The `answer` field must list **exactly the incorrect word(s)
   or phrase(s)** with their indices.
   - These must appear among the `choices`.

8. The `explanation` field must contain
   the validated **correct sentence** from step 1 (without indices).

9. The `tags` field must list the **actual error types introduced**
   (e.g., "verb tense", "article", "vocabulary",
   "singular/plural", "sentence structure", "connector misuse").

Follow these rules strictly to avoid connector redundancy
and other common grammatical mistakes.
"""
