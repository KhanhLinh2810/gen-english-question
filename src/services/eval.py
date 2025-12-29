import math
from typing import Any, Dict, List, Optional

import spacy
nlp = spacy.load("en_core_web_md")
import language_tool_python
tool = language_tool_python.LanguageTool('en-US')

import re
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity

from src.services.AI.false_ans_generator import FalseAnswerGenerator
from src.interfaces.evaluation import GeneratedQuestion  
from src.enums import QuestionTypeEnum
from src.loaders.elastic import Elastic
from env import config



class QuestionQualityEvaluator:
    INDEX = "vocabulary"

    def __init__(self):
        self._grammar_tool = tool
        self.nlp = nlp

        # Cache các config để dễ đọc
        self.weights = config["evaluation"]["weights"]
        self.penalties = config["evaluation"]["penalty_for_error"]["structure"]
        self.distractor_cfg = config["evaluation"]["distractor"]

    def evaluate(self, q: GeneratedQuestion, check_by_ai: bool = False) -> Dict[str, Any]:
        all_issues: List[Dict[str, Any]] = []
        all_suggestions: List[str] = []

        # 1. Structure
        s_score, s_issues, s_suggestions = self._check_structure(q)
        all_issues.append({"field": "structure", "score": s_score, "issues": s_issues})
        all_suggestions.extend(s_suggestions)

        # 2. Popularity
        p_score = self._check_popularity(q)
        all_issues.append({"field": "popularity", "score": p_score, "issues": []})

        # 3. Distractor
        d_score, d_issues = self._check_distractors(q)
        all_issues.append({"field": "distractor", "score": d_score, "issues": d_issues})

        w_score = self.weights["structure"] + self.weights["popularity"] + self.weights["distractor"] + self.weights["ai_adjust_factor"] if check_by_ai else 0.0
        final_score = (
            s_score * self.weights["structure"] +
            p_score * self.weights["popularity"] +
            d_score * self.weights["distractor"]
        ) / w_score

        rounded_score = math.ceil(final_score * 10) / 10

        return {
            "score": min(round(rounded_score, 1), 10.0),
            "issues": all_issues,
            "suggestions": list(set(all_suggestions))
        }

    def _check_structure(self, q: GeneratedQuestion):
        issues: List[Any] = []
        suggestions: List[str] = []
        score = 1.0

        # Question text
        if not q.content or not q.content.strip():
            issues.append("missing_question_text")
            score -= self.penalties["missing_question_text"]
        else:
            grammar_count, grammar_msgs = self._check_grammar(q.content)
            if grammar_count > 0:
                issues.append({
                    "type": "question_grammar_error",
                    "count": grammar_count,
                    "details": grammar_msgs
                })
                score -= grammar_count * self.penalties["grammar_error_per_count"]

        # Choices
        if not q.choices or len(q.choices) == 0:
            issues.append("missing_choices")
            score -= self.penalties["missing_choices"]
        else:
            empty_count = 0
            unique_contents = []
            has_correct = False

            for choice in q.choices:
                content = (choice.content or "").strip()
                if not content:
                    empty_count += 1
                    continue
                unique_contents.append(content)
                if choice.is_correct:
                    has_correct = True

            if empty_count > 0:
                issues.append(f"{empty_count}_empty_choices")
                score -= self.penalties["empty_choice_ratio"] * (empty_count / len(q.choices))

            if len(set(unique_contents)) < len(unique_contents):
                issues.append("duplicated_choices")
                score -= self.penalties["duplicated_choices"]

            if not has_correct:
                issues.append("no_correct_answer")
                score -= self.penalties["no_correct_answer"]

            for content in unique_contents:
                grammar_count, grammar_msgs = self._check_grammar(content)
                if grammar_count > 0:
                    issues.append({
                        "type": "choice_grammar_error",
                        "choice": content,
                        "count": grammar_count,
                        "details": grammar_msgs
                    })
                    score -= grammar_count * self.penalties["grammar_error_per_count"]

        return max(score, 0.0), issues, suggestions

    def _check_popularity(self, q: GeneratedQuestion) -> float:
        unique_words = set(q.content.lower().split())
        for choice in q.choices or []:
            unique_words.update((choice.content or "").lower().split())

        if not unique_words:
            return 0.0

        es = Elastic()
        resp = es.search(
            index=self.INDEX,
            size=0,
            query={"terms": {"word.keyword": list(unique_words)}},
            aggs={
                "by_word": {
                    "terms": {"field": "word.keyword", "size": len(unique_words)},
                    "aggs": {"cefr_level": {"avg": {"field": "cefr"}}}
                }
            }
        )

        word_cefr_map = {
            bucket["key"].lower(): bucket["cefr_level"]["value"] or 4.0
            for bucket in resp["aggregations"]["by_word"]["buckets"]
        }

        total = sum(word_cefr_map.get(word, 4.0) for word in unique_words)
        avg_cefr = total / len(unique_words)

        # Score cao khi từ khó hơn (CEFR cao hơn)
        popularity_score = max(0.0, (avg_cefr - 1) / 5.0)
        return round(popularity_score, 3)

    def _check_distractors(self, q: GeneratedQuestion):
        issues: List[Dict[str, Any]] = []
        scores: List[float] = []

        # 1. POS & lexical family
        pos_score = self._check_pos_and_meaning_of_choice(q)
        if pos_score is not None:
            scores.append(pos_score)
            issues.append({"type": "pos_lexical_family", "score": round(pos_score, 3)})

        # 2. Embedding similarity
        emb_score = self._cal_score_embedding_similarity(q)
        if emb_score is not None:
            scores.append(emb_score)
            t = self.distractor_cfg["embedding_similarity_thresholds"]
            level = (
                "too_different" if emb_score <= t["too_different"] else
                "moderate" if emb_score <= t["moderate"] else
                "good" if emb_score <= t["good"] else
                "strong" if emb_score <= t["strong"] else
                "excellent"
            )
            
            issues.append({
                "type": "embedding_similarity",
                "score": round(emb_score, 3),
                "level": level
            })

        # 3. Paragraph difficulty
        para_score = self._cal_score_for_paragraph(q)
        if para_score is not None:
            scores.append(para_score)
            diff_part = (para_score - self.distractor_cfg["paragraph"]["length_weight"]) / self.distractor_cfg["paragraph"]["difficulty_weight"] * 5
            level = "direct_match" if diff_part < 2 else "paraphrase" if diff_part < 4 else "inference"
            issues.append({
                "type": "paragraph_difficulty",
                "score": round(para_score, 3),
                "level": level
            })

        final_score = sum(scores) / len(scores) if scores else 0.0
        if scores:
            issues.append({
                "type": "distractor_summary",
                "score": round(final_score, 3),
                "components": len(scores)
            })

        return round(final_score, 3), issues

    def _check_grammar(self, text: str, max_errors: int = 5):
        if not text or len(text.strip()) < 5:
            return 0, []

        matches = self._grammar_tool.check(text)
        serious_matches = [
            m for m in matches
            if m.ruleIssueType in {"grammar", "misspelling"}
            and not m.ruleId.startswith("UPPERCASE_SENTENCE_START")
        ]

        error_messages = [
            {
                "message": m.message,
                "rule": m.ruleId,
                "error_text": text[m.offset:m.offset + m.errorLength],
                "suggestions": m.replacements[:3]
            }
            for m in serious_matches[:max_errors]
        ]
        return len(error_messages), error_messages

    def _check_pos_and_meaning_of_choice(self, q: GeneratedQuestion) -> Optional[float]:
        if q.type in {QuestionTypeEnum.PRONUNCIATION, QuestionTypeEnum.STRESS}:
            return 1.0

        to_be_regex = re.compile(
            r'\b(has been|have been|had been|will be|am|is|are|was|were|be|being|been|\'s|\'re|\'m)\b',
            flags=re.IGNORECASE
        )

        cleaned_choices: List[str] = []
        score = 1.0

        for c in q.choices or []:
            content = (c.content or "").strip()
            if not content:
                score -= self.distractor_cfg["empty_choice_deduction"]
                continue
            cleaned = to_be_regex.sub("", content)
            cleaned = " ".join(cleaned.split()).lower()
            cleaned_choices.append(cleaned)

        if any(len(t.split()) > 1 for t in cleaned_choices):
            return score

        docs = [self.nlp(text) for text in cleaned_choices]
        tokens = [token for doc in docs for token in doc]

        return score * self.lexical_family_difficulty(tokens, q.num_ans_per_question or 4)

    def _cal_score_embedding_similarity(self, q: GeneratedQuestion) -> Optional[float]:
        if q.type not in {QuestionTypeEnum.SYNONYM, QuestionTypeEnum.ANTONYM, QuestionTypeEnum.VOCAB}:
            return None

        correct = [c.content for c in q.choices if c.is_correct]
        distractors = [c.content for c in q.choices if not c.is_correct]
        if not correct or not distractors:
            return 0.0

        ai = FalseAnswerGenerator()
        emb_correct = ai.get_embedding_list_word(correct)
        emb_dist = ai.get_embedding_list_word(distractors)

        similarities = [
            cosine_similarity(c.reshape(1, -1), d.reshape(1, -1))[0][0]
            for c in emb_correct for d in emb_dist
        ]
        if not similarities:
            return 0.0

        avg_sim = sum(similarities) / len(similarities)
        t = self.distractor_cfg["embedding_similarity_thresholds"]

        if avg_sim <= t["too_different"]:
            return 0.2
        elif avg_sim <= t["moderate"]:
            return 0.4
        elif avg_sim <= t["good"]:
            return 0.6
        elif avg_sim <= t["strong"]:
            return 0.8
        else:
            return 1.0

    def _cal_score_for_paragraph(self, q: GeneratedQuestion) -> Optional[float]:
        if q.type not in {
            QuestionTypeEnum.VOCAB, QuestionTypeEnum.FACT,
            QuestionTypeEnum.MAIN_IDEA, QuestionTypeEnum.INFERENCE,
            QuestionTypeEnum.PURPOSE
        }:
            return None

        correct_answer = next((c.content for c in q.choices if c.is_correct), None)
        if not correct_answer or not q.paragraph:
            return 0.0

        words = q.paragraph.lower().split()
        word_count = len(words)
        p_cfg = self.distractor_cfg["paragraph"]

        # Length score
        if q.type == QuestionTypeEnum.VOCAB:
            thresholds = p_cfg["vocab_length_thresholds"]
            scores = [0.2, 0.3, 0.4, 0.5]
        else:
            thresholds = p_cfg["other_length_thresholds"]
            scores = [0.3, 0.5, 0.7, 0.9, 1.0]

        length_score = scores[-1]
        for thresh, sc in zip(thresholds, scores):
            if word_count <= thresh:
                length_score = sc
                break

        # Difficulty score
        doc = self.nlp(q.paragraph)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        if not sentences:
            return length_score * p_cfg["length_weight"]

        ai = FalseAnswerGenerator()
        sent_embs = ai.get_embedding_list_word(sentences)
        ans_emb = ai.get_embedding_list_word([correct_answer])

        cos_scores = cosine_similarity(ans_emb, sent_embs)[0]
        max_sim = float(max(cos_scores)) if cos_scores.size else 0.0

        levels = p_cfg["difficulty_levels"]
        if max_sim >= p_cfg["direct_match_sim"]:
            diff_val = levels[0]
        elif max_sim >= p_cfg["paraphrase_sim"]:
            diff_val = levels[1]
        else:
            diff_val = levels[2]

        diff_score = diff_val / 5.0

        return p_cfg["length_weight"] * length_score + p_cfg["difficulty_weight"] * diff_score

    def group_by_lemma(self, tokens):
        groups = defaultdict(list)
        for t in tokens:
            groups[t.lemma_.lower()].append(t)
        return groups

    def group_by_pos(self, tokens):
        groups = defaultdict(list)
        for t in tokens:
            groups[t.pos_].append(t)
        return groups

    def lexical_family_difficulty(self, tokens, num_ans_per_question: int = 4) -> float:
        if not tokens:
            return self.distractor_cfg["lexical_family"]["scores"]["low"]

        lemma_groups = self.group_by_lemma(tokens)
        pos_groups = self.group_by_pos(tokens)
        n = len(tokens)

        lemma_score = sum(len(v) for v in lemma_groups.values() if len(v) >= 3)
        lemma_ratio = lemma_score / n

        pos_score = sum(len(v) for v in pos_groups.values() if len(v) >= min(num_ans_per_question, 3))
        pos_ratio = pos_score / n

        t = self.distractor_cfg["lexical_family"]["thresholds"]
        s = self.distractor_cfg["lexical_family"]["scores"]

        if lemma_ratio >= t["high_lemma"]:
            return s["high_lemma"]
        if pos_ratio >= t["high_pos"]:
            return s["high_pos"]
        if pos_ratio >= t["medium_high_pos"]:
            return s["medium_high_pos"]
        if lemma_ratio >= t["medium_lemma"]:
            return s["medium_lemma"]
        if pos_ratio >= t["medium_both"] and lemma_ratio >= t["medium_both"]:
            return s["medium_both"]
        return s["low"]