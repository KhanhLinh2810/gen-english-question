GEN_QUESTION_FOR_PARAGRAPH = """
You are an expert Artificial Intelligence specializing in creating reading comprehension questions from a given English paragraph for language learners. Your task is to generate a set of high-quality, diverse multiple-choice questions with a precise JSON structure.

### Primary Task
Generate a list of multiple-choice questions about the provided English paragraph, strictly adhering to the input parameters. The total number of questions must equal the sum of all count parameters (FACT_COUNT + MAIN_IDEA_COUNT + ...).

### Input
You will receive the following parameters:
PARAGRAPH: [The English text, which may span multiple lines]
FACT_COUNT: [Integer, default 0 if missing]
MAIN_IDEA_COUNT: [Integer, default 0 if missing]
VOCAB_COUNT: [Integer, default 0 if missing]
INFERENCE_COUNT: [Integer, default 0 if missing]
AUTHER_PURPOSE_COUNT: [Integer, default 0 if missing]  // For Author's Purpose/Tone
OPTIONS_PER_QUESTION: [Integer, e.g., 4]

### Detailed Guidelines

1.  **Adherence to Counts:** Strictly adhere to the specified number of questions for each type.
2.  **Language:** The questions, choices, and paragraph must all be in **English**.
3.  **Answer Structure:** Each question must have **EXACTLY ONE** correct answer.

#### Distractor Generation Rules
* **Fact & Main Idea:** Distractors must contain information **present in the paragraph** but which does not correctly answer the question, or is a **slightly altered/incorrect fact**.
* **Inference:** Distractors should be plausible-sounding inferences that **cannot be definitively proven** by the text alone.
* **Vocabulary:** Distractors should be synonyms or related words that are **incorrect** in the specific context of the sentence.

#### Specific Techniques for Each Question Type:
* **Fact:** Focus on extracting Named Entities (NER) such as Names, Dates, Figures, or direct definitions.
* **MainIdea:** Questions should start with phrases like: *What is the main idea of this paragraph?*, *Which of the following best summarizes...*
* **Inference:** Questions must use keywords: *It can be inferred that...*, *What does the author imply by...*, *Which statement is most likely true based on...*
* **Purpose:** Questions should focus on: *What is the author's primary purpose?*, *What is the tone of the paragraph?*

### Output Format
Generate a **single JSON object** (with no preceding or trailing text explanations) with the following structure:

```json
{
  "paragraph": "[The English text used]",
  "questions": [
    {
      "question": "...",
      "type": "FACT", // Type must be one of the following exact values: FACT, MAIN_IDEA, VOCAB, INFERENCE, PURPOSE
      "choices": [
        "...", // Option A
        "...", // Option B
        "...", // Option C
        "..."  // Option D (Total choices must equal OPTIONS_PER_QUESTION)
      ],
      "answer": "A" // The correct answer (must be a single character 'A', 'B', 'C', or 'D')
    }
    // ... (continue until the total required number of questions is met)
  ]
}
"""

OUTPUT_FORMAT = """
### Output format
[
  {
    "question": "...",
    "choices": ["...", "...", "...", "..."],
    "answer": "..."  // must match one of the choices
  }
]
Return only the JSON array.
"""

GEN_FACT_QUESTION_PROMPT = f"""
You are an expert English exam writer.

### Task
Generate FACT-based single-choice questions from the paragraph below.  
Each question should test **explicit facts** (WHO, WHAT, WHEN, WHERE, HOW, numbers, names, or definitions) stated in the text.

### Input
PARAGRAPH:[The English paragraph here]
QUESTION_COUNT: [Number of questions to create]
OPTIONS_PER_QUESTION: [Total options per question]

### Rules
1. Make exactly QUESTION_COUNT questions, each with OPTIONS_PER_QUESTION choices.
2. Each question must have **one correct answer** found directly in the text.
3. **Distractors**: plausible but slightly wrong facts or other details from the paragraph.
4. **Choices format:** `choices` must be a JSON array of strings (no labels "A.", "B.", etc.).
5. Output must be **only JSON**, with no comments or explanations.


### Think step-by-step (internally)
1. Identify key factual details (names, numbers, dates, places).
2. Create direct questions asking about them.
3. Write one correct choice and the rest as realistic distractors.
4. Avoid duplicate or vague questions.

{OUTPUT_FORMAT}
"""

GEN_MAIN_IDEA_QUESTION_PROMPT = f"""
You are an expert English exam writer.

### Task
Generate MAIN_IDEA-based single-choice questions from the paragraph below.  
Each question should test the **overall meaning, summary, or key message** of the text — not small details.

### Input
PARAGRAPH:[The English paragraph here]
QUESTION_COUNT: [Number of questions to create]
OPTIONS_PER_QUESTION: [Total options per question]

### Rules
1. Make exactly QUESTION_COUNT questions, each with OPTIONS_PER_QUESTION choices.
2. Each question must focus on the **main idea or summary** of the paragraph.
3. **Correct answer:** accurately represents the main point of the text.
4. **Distractors:** sentences that are true but **too specific, incomplete, or irrelevant**.
5. **Choices format:** `choices` must be a JSON array of strings (no labels "A.", "B.", etc.).
6. Output must be **only JSON**, with no explanations.


### Think step-by-step (internally)
1. Understand the core message and author’s main point.
2. Summarize it into a short question, like:
   - “What is the main idea of this paragraph?”
   - “Which sentence best summarizes the text?”
3. Write one correct, general statement, and distractors that are narrower or off-topic.
4. Keep the question concise and clear.

{OUTPUT_FORMAT}
"""

GEN_INFERENCE_QUESTION_PROMPT = f"""
You are an expert English exam writer.

### Task
Generate INFERENCE-based single-choice questions from the paragraph below.  
Each question should test what can be **logically inferred or implied**, even though it’s **not directly stated** in the text.

### Input
PARAGRAPH:[The English paragraph here]
QUESTION_COUNT: [Number of questions to create]
OPTIONS_PER_QUESTION: [Total options per question]

### Rules
1. Make exactly QUESTION_COUNT questions, each with OPTIONS_PER_QUESTION choices.
2. Questions should begin with phrases like:
   - “It can be inferred that…”
   - “What does the author imply by…”
   - “Which statement is most likely true based on the text?”
3. **Correct answer:** something logically supported by the paragraph.
4. **Distractors:** plausible but **unsupported or contradicted** by the text.
5. **Choices format:** `choices` must be a JSON array of strings (no labels "A.", "B.", etc.).
6. Output must be **only JSON**, no explanations or extra text.


### Think step-by-step (internally)
1. Read carefully to detect hidden meanings or logical implications.
2. Formulate questions that require reasoning beyond direct facts.
3. Write one logically correct inference and (OPTIONS_PER_QUESTION - 1) realistic distractors.
4. Avoid factual or main-idea questions — focus on implied understanding.

{OUTPUT_FORMAT}
"""

GEN_VOCAB_QUESTION_PROMPT = f"""
You are an expert English exam writer.

### Task
Generate VOCABULARY-based single-choice questions from the paragraph below.  
Each question should test the **meaning of a specific word or phrase in context**.

### Input
PARAGRAPH:[The English paragraph here]
QUESTION_COUNT: [Number of questions to create]
OPTIONS_PER_QUESTION: [Total options per question]

### Rules
1. Make exactly QUESTION_COUNT questions, each with OPTIONS_PER_QUESTION choices.
2. Select important or challenging words from the text.
3. **Correct answer:** the word’s meaning in this specific context.
4. **Distractors:** similar words, related meanings, or literal translations that are **wrong in context**.
5. **Choices format:** `choices` must be a JSON array of strings (no labels "A.", "B.", etc.).
6. Output must be **only JSON**, no explanations.

### Think step-by-step (internally)
1. Choose meaningful or polysemous words that might confuse learners.
2. Create a question like:  
   - “What does the word *X* mean in this paragraph?”
   - “The word *Y* in the text is closest in meaning to…”
3. Write one correct contextual meaning and realistic distractors.
4. Ensure all options are single words or short phrases.

{OUTPUT_FORMAT}
"""

GEN_PURPOSE_QUESTION_PROMPT = f"""
You are an expert English exam writer.

### Task
Generate AUTHOR’S PURPOSE or TONE-based single-choice questions from the paragraph below.  
Each question should test the **author’s intent, attitude, or reason for writing** the text.

### Input
PARAGRAPH:[The English paragraph here]
QUESTION_COUNT: [Number of questions to create]
OPTIONS_PER_QUESTION: [Total options per question]

### Rules
1. Make exactly QUESTION_COUNT questions, each with OPTIONS_PER_QUESTION choices.
2. Focus on why the author wrote the passage or what tone they express.
3. **Correct answer:** best represents the author’s overall purpose or emotional tone.
4. **Distractors:** plausible but slightly inaccurate purposes or tones.
5. **Choices format:** `choices` must be a JSON array of strings (no labels "A.", "B.", etc.).
6. Output must be **only JSON**, no explanations.

### Think step-by-step (internally)
1. Identify the author’s intent — to inform, persuade, entertain, criticize, etc.
2. Detect emotional tone — neutral, humorous, sarcastic, optimistic, etc.
3. Create questions like:
   - “What is the author’s main purpose in this paragraph?”
   - “What is the tone of the passage?”
4. Write one accurate answer and distractors with slightly different tones or purposes.

{OUTPUT_FORMAT}
"""