from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.services.eval import QuestionQualityEvaluator
from src.factories.gen_question.factory import create_question_instance
from src.factories.gen_question_for_paragraph.factory import create_question_paragraph_instance
from src.utils.response import res_ok
# from src.utils.text_process import vietnamese_to_english, english_to_vietnamese, get_all_summary, get_all_questions
from src.interfaces.question import ModelInput, ICreateQuestion, ICreateQuestionForParagraph
# from src.services.AI.abstractive_summarizer import AbstractiveSummarizer
# from src.services.AI.question_generator import QuestionGenerator    
# from src.services.AI.false_ans_generator import FalseAnswerGenerator
# from src.services.AI.keyword_extractor import KeywordExtractor

route = APIRouter(prefix="/question", tags=["Question"])
print("Including question routes...")

@route.post('/')
async def generate_question(body: ICreateQuestion):
    question = create_question_instance(body.type)
    list_questions = question.generate_questions(
        list_words=body.list_words,
        num_question=body.num_question,
        num_ans_per_question=body.num_ans_per_question,
    )
    print("+++++", list_questions)
    evaluator = QuestionQualityEvaluator()
    final_data = []
    for q in list_questions:
        data = {**body.model_dump(), **q} 
        
        score = evaluator.evaluate(data)
        data["score"] = score 
        final_data.append(data)
        
    return JSONResponse(status_code=200, content=res_ok(final_data))

@route.post('/sentence')
async def generate_questions_from_sentence(body: ICreateQuestionForParagraph):
    evaluator = QuestionQualityEvaluator()
    print(evaluator._grammar_tool(body.paragraph))
    # error_sentences = []
    # model_input = ModelInput(**body.model_dump(), user_id=None)
    # try:
    #     new_questions =  generate_and_store_questions(model_input)
    # except Exception as e:
    #     # Không để là model_input.context mà là request.context vì model_input.context là tiếng Anh
    #     print(f"Lỗi khi xử lí câu: {body.context}. Lỗi: {e}")
    #     error_sentences.append({'sentence': body.context, 'error': str(e)})

    # result = {
    #     "success": new_questions,
    #     "fail": error_sentences
    # }
    question = create_question_paragraph_instance()
    list_questions = question.generate_questions(data=body)
    return JSONResponse(status_code=200, content=res_ok(list_questions))

# async def generate_and_store_questions(self, request):
#         """Generate questions from user request and store results in Firestore.

#         Args:
#             request (ModelInput): request from flutter.

#         Returns:
#             dict: results saved to Firestore
#         """
#         request.context = vietnamese_to_english(request.context)
#         request.name = vietnamese_to_english(request.name)

#         await self.user_repo.update_generator_working_status(request, True)
#         questions, crct_ans, all_ans = await self.generate_questions_and_answers(request.context)
#         await self.user_repo.update_generator_working_status(request, False)

#         results = self.send_results_to_db(request, questions, crct_ans, all_ans, request.context)
#         return results

# def generate_questions_and_answers(context: str):
        # """Generate questions and answers from given context.

        # Args:
        #     context (str): input corpus used to generate question.

        # Returns:
        #     tuple[list[str], list[str], list[list[str]]]:
        #     questions, correct answers, and all answer choices.
        # """
        # summarizer = AbstractiveSummarizer()
        # question_gen = QuestionGenerator()
        # false_ans_gen = FalseAnswerGenerator()
        # keyword_extractor = KeywordExtractor()
        # summary, splitted_text = get_all_summary(
        #     model=summarizer, context=context
        # )
        # filtered_kws = keyword_extractor.get_keywords(
        #     original_list=splitted_text, summarized_list=summary
        # )

        # crct_ans, all_answers = false_ans_gen.get_output(filtered_kws=filtered_kws)
        # questions = get_all_questions(
        #     model=question_gen, context=summary, answer=crct_ans
        # )

        # return questions, crct_ans, all_answers