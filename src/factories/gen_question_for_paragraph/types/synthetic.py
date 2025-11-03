from src.enums import ParagraphQuestionTypeEnum
from src.interfaces.question import ICreateQuestionForParagraph
from src.factories.gen_question_for_paragraph.types.base import Question
from src.llms.models import GeminiLLM
from src.llms.prompts import GEN_FACT_QUESTION_PROMPT, GEN_MAIN_IDEA_QUESTION_PROMPT, GEN_PURPOSE_QUESTION_PROMPT, GEN_INFERENCE_QUESTION_PROMPT, GEN_VOCAB_QUESTION_PROMPT
from src.llms.tools import GEN_QUESTION_FOR_PARAGRAPH_OUTPUT_TOOL


class ParagraphQuestion(Question):
    def __init__(self):
        self.llm = GeminiLLM()

    def generate_questions(self, data: ICreateQuestionForParagraph):
        result = []
        type_to_prompt_map = {
            ParagraphQuestionTypeEnum.FACT: GEN_FACT_QUESTION_PROMPT,
            ParagraphQuestionTypeEnum.MAIN_IDEA: GEN_MAIN_IDEA_QUESTION_PROMPT,
            ParagraphQuestionTypeEnum.VOCAB: GEN_VOCAB_QUESTION_PROMPT,
            ParagraphQuestionTypeEnum.INFERENCE: GEN_INFERENCE_QUESTION_PROMPT,
            ParagraphQuestionTypeEnum.PURPOSE: GEN_PURPOSE_QUESTION_PROMPT,
        }

        type_to_total_count = {}
        for question_data in data.list_create_question:
            qtype = question_data.question_type
            num = question_data.num_question
            type_to_total_count[qtype] = type_to_total_count.get(qtype, 0) + num

        final_output = {}
        for qtype, total_count in type_to_total_count.items():
            prompt = type_to_prompt_map.get(qtype)
            if not prompt:
                continue

            content_user = (
                f"PARAGRAPH: {data.description}\n"
                f"QUESTION_COUNT: {total_count}\n"
                f"OPTIONS_PER_QUESTION: {data.num_ans_per_question}\n"
            )

            raw_output = self.llm.generate_response(
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content_user},
                ],
                tools=[GEN_QUESTION_FOR_PARAGRAPH_OUTPUT_TOOL],
            )

            self.process_raw_output_of_llm(raw_output, qtype, result)

        return result
    
    def process_raw_output_of_llm(self, raw_output, qtype, result):
        if not "tool_calls" in raw_output or not raw_output["tool_calls"]:
            return 
        for call in raw_output["tool_calls"]:
            if call.get("name") != "parse_paragraph_questions":
                continue
            data = call.get("arguments", {})

            for question in data.get("list_questions", []):
                result.append({
                    "question": question.get("question"),
                    "type": qtype,
                    "choices": question.get("choices", []),
                    "answer": question.get("answer"),
                })
