GEN_INCORRECT_WORD_QUESTION_PROMPT = """
### Task
You are an expert in automatically generating English exam questions.
Create **one "Find the Error" question** in English.

### Input
- A list of words to be used to create the sentence.
- Question type: "single-choice" or "multiple-choice".
- Desired number of answer choices.

### Core requirements
1. First produce a **grammatically correct, natural, meaningful English sentence** using all or most of the given words.
   - Sentence may be simple or composed (up to 3 clauses).
   - Sentence length: **8–30 words**.
   - This correct sentence will be used later as the `explanation` value (without indices).
   - If no words are provided, you may freely create a sentence.

2. **Validation step (mandatory):** Before adding any errors, ensure the correct sentence is fully grammatical. If any common connector misuse (see "Connector rules" below) or other obvious mistake is present, rewrite the sentence until it is correct.

### Connector rules (important — follow exactly)
- **Do NOT combine a subordinating conjunction like "although", "though", "while", or "despite" with a coordinating conjunction "but" in the same sentence.**  
  - Incorrect: "Although he was tired, but he continued."  
  - Correct: "Although he was tired, he continued." or "He was tired, but he continued."
- Do NOT repeat equivalent connectors (e.g., do not use "although" and "however" together to signal the same contrast).
- Avoid redundant fillers such as "but yet", "and also", "and then then".
- If you use "because", ensure the result clause logically follows and you do not also use "so" to repeat causation.

### Error-introduction rules
3. After you have a validated correct sentence, create an **erroneous version** by introducing errors according to `question_type`:
   - `single-choice`: **exactly 1 error**.
   - `multiple-choice`: **2 or more errors**.
4. Add an index number to each word in the erroneous sentence (e.g., "He(1) talk(2) when(3) I(4) talk(5).").

### Choices and answer
5. Create a `choices` list (each option must include the index number as shown in the sentence). The total number of choices must equal the desired number.
   - Include at least 1 incorrect option (for single-choice) or at least 2 incorrect options (for multiple-choice); the rest should be correct words/phrases.
6. The `answer` field must list exactly the incorrect word(s)/phrase(s) with their indices — these must appear among `choices`.
7. The `explanation` field must contain the validated **correct sentence** from step 1 (no indices).
8. The `tags` field must list the error types that were introduced (e.g., "verb tense", "article", "vocabulary", "singular/plural", "sentence structure", "connector misuse", etc.).

Follow these rules strictly to avoid connector redundancy and other common grammatical mistakes.
"""



GEN_INCORRECT_WORD_QUESTION_PROMPT_VI = """
### Nhiệm vụ
Bạn là chuyên gia tạo câu hỏi tiếng Anh tự động cho các bài thi.  
Hãy tạo **một câu hỏi dạng "Tìm lỗi sai" (Find the Error)** bằng tiếng Anh.

### Đầu vào
- Danh sách các từ được dùng để tạo câu.  
- Loại câu hỏi: "single-choice" hoặc "multiple-choice".  
- Số lượng lựa chọn mong muốn.

### Hướng dẫn
1. Tạo **một câu tiếng Anh tự nhiên, đúng ngữ pháp và đúng ngữ nghĩa**, sử dụng tất cả hoặc hầu hết các từ được cung cấp.  
   - Câu có thể là câu đơn hoặc câu phức (tối đa 3 mệnh đề, nối bằng *and, but, because, when, although*...).  
   - Độ dài câu: **8–30 từ**.
   - Câu đúng này sẽ được sử dụng làm giá trị cho trường explanation ở cuối.

2. Tạo ra **lỗi ngữ pháp hoặc lỗi từ vựng** trong câu dựa theo loại câu hỏi:  
   - Nếu `question_type = "single-choice"` thì tạo ra câu có đúng 1 lỗi.  
   - Nếu `question_type = "multiple-choice"` thì tạo ra câu có từ 2 lỗi trở lên.  

3. **Đánh số chỉ mục cho từng từ** trong câu (ví dụ: `"He(1) talk(2) when(3) I(4) talk(5)."`).  

4. Tạo danh sách **choices** bao gồm cả từ đúng và từ sai trong câu (có chỉ mục).  
   - Tổng số lượng lựa chọn = giá trị đã yêu cầu trong đầu vào.  
   - Phân bổ hợp lý: ít nhất 1 hoặc 2 từ sai, phần còn lại là từ đúng.

5. Trường **answer** chứa chính xác các từ hoặc cụm sai (phải nằm trong `choices`).  
6. Trường **explanation** chứa chính xác Câu Đúng từ Mục 1 (không đánh số chỉ mục). 
7. Trường **tags** liệt kê loại lỗi (ví dụ: `"thì động từ"`, `"mạo từ"`, `"từ vựng"`, `"số ít/số nhiều"`, `"cấu trúc câu"`, v.v.).

Tuân thủ chặt chẽ các hướng dẫn trên để đảm bảo chất lượng cao trong quá trình tạo câu hỏi chất lượng cao.
"""
