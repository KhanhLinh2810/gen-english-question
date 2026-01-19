import os
from dotenv import load_dotenv
import json

load_dotenv()

def env_float(key: str, default: float) -> float:
    try:
        return float(os.getenv(key, default))
    except (TypeError, ValueError):
        return default


def env_int_list(key: str, default: list[int]) -> list[int]:
    try:
        val = os.getenv(key)
        if val is None:
            return default
        return list(map(int, json.loads(val)))
    except Exception:
        return default
    
config = {
    "app": {
        'port': os.getenv("PORT"),
        'ignore_authen': os.getenv("IGNORE_AUTHEN", "false").lower() == "true",
    },
    "db": {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_DATABASE"),
        "pool_size": int(os.getenv("POOL_SIZE") or 8),
        "max_overflow": int(os.getenv("MAX_OVERFLOW") or 16),
        "pool_recycle": int(os.getenv("POOL_RECYCLE") or 800),
    },
    "jwt": {
        "expired_in": int(os.getenv("JWT_EXPIRATION_DELTA") or 24), # hour
        "algorithm": os.getenv("JWT_ALGORITHM"),
        "secret_key": os.getenv("JWT_SECRET"),
    },
    "google": {
        "api_key": os.getenv("GOOGLE_API_KEY"),
    },
    "open_ai": {
        "api_key": os.getenv("OPEN_AI_API_KEY", ""),
        "base_url": os.getenv("OPEN_AI_BASE_URL"),        
    },
    "elastic": {
        "url": os.getenv("ELASTIC_URL"),
        "api_key": os.getenv("ELASTIC_API_KEY")
    },
    "evaluation": {
        "weights": {
            "structure": env_float("WEIGHT_STRUCTURE", 0.2),
            "popularity": env_float("WEIGHT_POPULARITY", 0.2),
            "distractor": env_float("WEIGHT_DISTRACTOR", 0.4),
            "ai_adjust_factor": env_float("WEIGHT_AI_ADJUST_FACTOR", 0.8),
        },

        "penalty_for_error": {
            "structure": {
                "missing_question_text": env_float("PENALTY_MISSING_QUESTION_TEXT", 0.4),
                "missing_choice": env_float("PENALTY_MISSING_CHOICE", 0.2),
                "no_correct_answer": env_float("PENALTY_NO_CORRECT_ANSWER", 0.4),
                "empty_choice": env_float("PENALTY_EMPTY_CHOICE", 0.1),
                "duplicated_choices": env_float("PENALTY_DUPLICATED_CHOICES", 0.1),
                "grammar_error": env_float("PENALTY_GRAMMAR_ERROR", 0.05),
            }
        },

        "distractor": {
            "empty_choice_deduction": env_float("DISTRACTOR_EMPTY_CHOICE_DEDUCTION", 0.05),

            "embedding_similarity_thresholds": {
                "too_different": env_float("DISTRACTOR_EMBEDDING_SIMILARITY_TOO_DIFFERENT", 0.35),
                "moderate": env_float("DISTRACTOR_EMBEDDING_SIMILARITY_MODERATE", 0.45),
                "good": env_float("DISTRACTOR_EMBEDDING_SIMILARITY_GOOD", 0.6),
                "strong": env_float("DISTRACTOR_EMBEDDING_SIMILARITY_STRONG", 0.7),
            },

            "paragraph": {
                "length_weight": env_float("DISTRACTOR_PARAGRAPH_LENGTH_WEIGHT", 0.1),
                "difficulty_weight": env_float("DISTRACTOR_PARAGRAPH_DIFFICULTY_WEIGHT", 0.9),

                "vocab_length_thresholds": env_int_list(
                    "DISTRACTOR_PARAGRAPH_VOCAB_LENGTH_THRESHOLDS",
                    [50, 100, 200, 300]
                ),
                "other_length_thresholds": env_int_list(
                    "DISTRACTOR_PARAGRAPH_OTHER_LENGTH_THRESHOLDS",
                    [50, 100, 200, 300]
                ),

                "direct_match_sim": env_float("DISTRACTOR_PARAGRAPH_DIRECT_MATCH_SIM", 0.85),
                "paraphrase_sim": env_float("DISTRACTOR_PARAGRAPH_PARAPHRASE_SIM", 0.5),
                "difficulty_levels": env_int_list(
                    "DISTRACTOR_PARAGRAPH_DIFFICULTY_LEVELS",
                    [1, 3, 5]
                ),
            },

            "lexical_family": {
                "thresholds": {
                    "high_lemma": env_float("DISTRACTOR_LEXICAL_FAMILY_HIGH_LEMMA", 0.9),
                    "high_pos": env_float("DISTRACTOR_LEXICAL_FAMILY_HIGH_POS", 0.9),
                    "medium_high_pos": env_float("DISTRACTOR_LEXICAL_FAMILY_MEDIUM_HIGH_POS", 0.6),
                    "medium_lemma": env_float("DISTRACTOR_LEXICAL_FAMILY_MEDIUM_LEMMA", 0.7),
                    "medium_both": env_float("DISTRACTOR_LEXICAL_FAMILY_MEDIUM_BOTH", 0.4),
                    "low": env_float("DISTRACTOR_LEXICAL_FAMILY_LOW", 0.3),
                },
                "scores": {
                    "high_lemma": env_float("DISTRACTOR_LEXICAL_FAMILY_HIGH_LEMMA_SCORE", 0.75),
                    "high_pos": env_float("DISTRACTOR_LEXICAL_FAMILY_HIGH_POS_SCORE", 0.9),
                    "medium_high_pos": env_float("DISTRACTOR_LEXICAL_FAMILY_MEDIUM_HIGH_POS_SCORE", 0.7),
                    "medium_lemma": env_float("DISTRACTOR_LEXICAL_FAMILY_MEDIUM_LEMMA_SCORE", 0.6),
                    "medium_both": env_float("DISTRACTOR_LEXICAL_FAMILY_MEDIUM_BOTH_SCORE", 0.45),
                    "low": env_float("DISTRACTOR_LEXICAL_FAMILY_LOW_SCORE", 0.3),
                },
            },
        },
    }
}