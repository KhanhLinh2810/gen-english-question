from collections import defaultdict
from datetime import datetime
import json
from typing import Dict, List
import random
from src.services.mail.mail import create_json_file, send_json_email
from src.llms.prompts import VERIFY_ANSWER_BY_AI_PROMPT
from src.llms.tools import VERIFY_ANSWER_BY_AI_TOOL
from src.llms.models import GeminiLLM, OpenAILLM
from src.loaders.database import SessionLocal, AIQuestion
from src.enums.question import ParagraphQuestionTypeEnum, QuestionTypeEnum
from env import config
from sqlalchemy import Sequence, select

target_values = [e.value for e in [
    QuestionTypeEnum.INCORRECT_WORD,
    QuestionTypeEnum.FILL_IN_BLANK,
    QuestionTypeEnum.REARRANGE,
    QuestionTypeEnum.FACT,
    QuestionTypeEnum.MAIN_IDEA,
    QuestionTypeEnum.VOCAB,
    QuestionTypeEnum.INFERENCE,
    QuestionTypeEnum.PURPOSE
]]

async def verify_answer_by_ai():
    # print("Bắt đầu thực hiện task verify...")
    async with SessionLocal() as db:
        try:
            result = await db.execute(
                select(AIQuestion)
                .where(
                    AIQuestion.is_check_by_ai == False,
                    AIQuestion.type.in_(target_values)
                )
                .limit(500)
            )
            questions = result.scalars().all()

            if not questions:
                # print("Không có câu hỏi nào cần check.")
                return

            questions_by_type = classify_questions_by_type(questions)
            llm = GeminiLLM()
            # llm = OpenAILLM

            done_check_question = []
            report_data = {
                "timestamp": datetime.now().isoformat(),
                "checked_questions": 0,
                "incorrect_answers": 0,
                "correct_answers": 0,
                "questions": []
            }

            for _ in range(1):
                if not questions_by_type:
                    break

                random_type = random.choice(list(questions_by_type.keys()))
                bucket = questions_by_type[random_type]

                max_questions = 5 if random_type in ParagraphQuestionTypeEnum else 10
                selected_questions = bucket[:max_questions]
                questions_by_type[random_type] = bucket[max_questions:]

                if not questions_by_type[random_type]:
                    questions_by_type.pop(random_type)

                content = format_list_question(selected_questions)

                raw_output = llm.generate_response(
                    messages=[
                        {"role": "system", "content": VERIFY_ANSWER_BY_AI_PROMPT},
                        {"role": "user", "content": f"List of question:\n{content}"}
                    ],
                    tools=[VERIFY_ANSWER_BY_AI_TOOL],
                )

                result_llm = parse_raw_tool_output(raw_output)
                llm_map = {r["question_index"]: r for r in result_llm}

                for idx, question in enumerate(selected_questions):
                    llm_result = llm_map.get(idx)
                    if not llm_result:
                        continue

                    llm_choice_index = llm_result["answer"]

                    system_choice_index = next(
                        (i for i, c in enumerate(question.choices) if c.get("is_correct")),
                        None
                    )

                    if system_choice_index is None:
                        continue

                    if system_choice_index != llm_choice_index:
                        report_data["incorrect_answers"] += 1
                        question.is_correct_answer = False
                        question.correct_choice_index = llm_choice_index
                    else:
                        report_data["correct_answers"] += 1
                        question.is_correct_answer = True

                    question.is_check_by_ai = True

                done_check_question.extend(selected_questions)


            await db.commit()

            if len(done_check_question) > 0:
                report_data["checked_questions"] = len(done_check_question)
                report_data["questions"] = json.dumps([q.to_dict() for q in done_check_question], 
                                    ensure_ascii=False, indent=2)
                send_report(report_data)

        except Exception as e:
            await db.rollback()
            print(f"Lỗi trong quá trình verify: {e}")
def format_list_question(questions: Sequence[AIQuestion]) -> str:
    result = ""

    for i, q in enumerate(questions, start=1):
        content = f"\nQuestion {i}: {q.content}\n"

        if q.type in ParagraphQuestionTypeEnum and getattr(q, "paragraph", None):
            content = f"Paragraph: {q.paragraph}\n" + content

        for j, c in enumerate(q.choices):
            label = chr(ord('A') + j)
            content += f"{label}. {c['content']}\n"

        result += content + "\n"

    return result

def classify_questions_by_type(
    questions: Sequence[AIQuestion],
) -> Dict[int, List[AIQuestion]]:
    questions_by_type = defaultdict(list)

    for question in questions:
        questions_by_type[question.type].append(question)

    return questions_by_type

def parse_raw_tool_output(raw_output):
    results = []

    if not raw_output or "tool_calls" not in raw_output:
        return results

    for call in raw_output["tool_calls"]:
        if call.get("name") != VERIFY_ANSWER_BY_AI_TOOL["function"]["name"]:
            continue

        items = call.get("arguments", {}).get("results", [])
        for item in items:
            question_index = item["question_index"] - 1  # convert to 0-based
            answer_label = item["correct_answer"]
            answer_index = ord(answer_label) - ord("A")

            results.append({
                "question_index": question_index,
                "answer": answer_index,
                "confidence": item.get("confidence"),
                "note": item.get("note")
            })

    return results

def send_report(json_data):
    subject = "Báo cáo kiểm tra đáp án bằng AI"
    body_content = f"""
Đây là báo cáo hàng ngày về kiểm tra đáp án bằng LLM.

Thời gian: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Số câu đã kiểm tra: {json_data["checked_questions"]}
Số câu đúng: {json_data["correct_answers"]}
Số câu sai: {json_data["incorrect_answers"]}
Tỷ lệ chính xác: {json_data["correct_answers"]/json_data["checked_questions"]*100 if json_data["checked_questions"] > 0 else 0:.2f}%
"""
    
    # Tạo file JSON đính kèm
    attachment = create_json_file(json_data, f"report_duplicheck_answer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    # Gửi email
    send_json_email(
        config["email"]["report"]["llm_email"], 
        subject, 
        body_content, 
        attachment
    )