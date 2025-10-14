"""This module handles all textual preprocessing tasks, all textual postprocessing tasks.

@Author: Karthick T. Sharma
"""

import re
from deep_translator import GoogleTranslator
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')



def filter_text(context):
    """Remove all signs other than -,-,a-z,A-Z,0-9, and some symbols.....
    and remove all extra blank spaces.

    Args:
        text (str): input string for processing.

    Returns:
        str: processed string.
    """
    text = context.strip()
    text = re.sub('[\u2010-\u2013]', '-', text)
    text = re.sub(r'[^a-zA-Z0-9\.,-?%&*()]', ' ', text)
    text = re.sub(' {2,}', ' ', text)
    return text


def split_text(context, char_range=300):
    """Split the bulk input text into small chunks.

    Args:
        text (str): processed string to be splitted.

    Returns:
        list[str]: list of splitted corpus.
    """
    bulk_text = filter_text(context=context)

    if len(bulk_text) <= char_range:
        return [bulk_text]

    splitted_texts = []
    # split whole input into $(char_range) block of meaningful text.
    # (only split after an full stop has encountered)
    while len(bulk_text) > char_range:
        i = char_range
        while((i < len(bulk_text)) and (bulk_text[i] != '.')):
            i += 1
        splitted_texts.append(bulk_text[:(i+1)])
        bulk_text = bulk_text.replace(bulk_text[:(i+1)], "")
    return splitted_texts


def change_format(false_ans):
    """Change s2v format to fair readable form. Remove '|,_' and toggle case.

    Args:
        false_ans (list[tuple(str,int)]): list of most similar words and their
        similiarity.

    Returns:
        list[str]: false_ans in fair-readable format.
    """
    output = []
    for result in false_ans:
        res = result[0].split('|')
        res = res[0].replace('_', ' ')
        res = res[0].upper() + res[1:]
        output.append(res)
    return output

def postprocess_summary(text):
    """Postprocess the output of summarizer model for fair readable output.

       Capitalize firt word of sentence. Put spaces in required place.

    Args:
        text (str): summarized text to processed.

    Returns:
        str: clean-human readable text.
    """
    output = ""

    for token in sent_tokenize(text):
        token = token.capitalize()
        output += " " + token
    return output


def postprocess_question(text):
    """Postprocess the output of question generation model for fair readable.

    Args:
        text (text): generated question to be processed.

    Returns:
        str: clean readable text.
    """
    output = text.replace("question: ", "")
    output = output.strip()
    return output

# Dịch vietnamese -> english
def vietnamese_to_english(text):
    translator = GoogleTranslator(source='vi', target='en')
    translated_text = translator.translate(text)
    return translated_text

def english_to_vietnamese(text):
    translator = GoogleTranslator(source='en', target='vi')
    translated_text = translator.translate(text)
    return translated_text


def get_all_summary(model, context):
    """Generate summary of input corpus.

    Args:
        model (OnnxT5): T5 transformer for summarization.
        context (str): Bunch of unprocessed text.

    Returns:
        tuple(list(str), list(str)): tuple of, list of summarized text chunks and list of
        original text chuncks.
    """
    summary = []
    splitted_text = model.preprocess_input(context)

    for txt in splitted_text:
        summary.append(model.summarize(txt))

    return summary, splitted_text


def get_all_questions(model, context, answer):
    """Return list of generated questions.

    Args:
        model (OnnxT5): T5 transformer for question generation.
        context (list(str)): list of context for generating questions.
        answer (list(str)): list of answers for question which will be generated.

    Returns:
        list(str): list of questions within given context
    """
    questions = []

    for cont, ans in zip(context, answer):
        questions.append(model.generate(cont, ans))

    # squeezing the 2d list to 1d
    return questions
