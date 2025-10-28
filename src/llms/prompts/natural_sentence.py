GEN_NATURAL_SENTENCE_PROMPT = """
### Task
You are an expert English sentence generator.
Your task is to create **one natural, grammatically correct, and meaningful English sentence**.

### Input
- A list of English words that should appear in the sentence (if provided).

### Requirements
1. Use **all or most** of the given words naturally and in the correct grammatical order.  
   - If no words are provided, freely create a natural sentence on any general topic.
2. The sentence must:
   - Be **fully grammatical and fluent**.
   - Contain **8–20words**.
   - Be **coherent** (logical meaning, not random).
   - Sound **natural** as if written by a native English speaker.
3. Allowed topics: everyday life, travel, work, study, hobbies, nature, or simple human experiences.
4. Avoid:
   - Unnecessary repetition.
   - Connector misuse (e.g., “Although … but …”).
   - Unnatural collocations or incomplete clauses.

### Output
Return **only one English sentence** that satisfies the above requirements.
"""
