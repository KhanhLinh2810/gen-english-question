import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "app": {
        'port': os.getenv("PORT"),
    },
    "db": {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_DATABASE"),
        "pool_size": int(os.getenv("POOL_SIZE")) | 8,
        "max_overflow": int(os.getenv("MAX_OVERFLOW")) | 16,
        "pool_recycle": int(os.getenv("POOL_RECYCLE")),
    },
    "jwt": {
        "expired_in": int(os.getenv("JWT_EXPIRATION_DELTA")) | 24, # hour
        "algorithm": os.getenv("JWT_ALGORITHM"),
        "secret_key": os.getenv("JWT_SECRET"),
    },
    "google": {
        "api_key": os.getenv("GOOGLE_API_KEY"),
    },
    "elastic": {
        "url": os.getenv("ELASTIC_URL"),
        "api_key": os.getenv("ELASTIC_API_KEY")
    },
    "evalution" : {
        "weights": {
            "structure": os.getenv("WEIGHT_STRUCTURE") | 0.2,
            "popularity": os.getenv("WEIGHT_POPULARITY") | 0.2,
            "distractor": os.getenv("WEIGHT_DISTRACTOR") | 0.4,
            "ai_adjust_factor": os.getenv("WEIGHT_AI_ADJUST_FACTOR") | 0.8   
        },
        "penalty_for_error" : {
            "structure" : {
                "missing_question_text": os.getenv("PENALTY_MISSING_QUESTION_TEXT") | 0.4,
                "missing_choice": os.getenv("PENALTY_MISSING_CHOICE") | 0.2,
                "no_correct_answer": os.getenv("PENALTY_NO_CORRECT_ANSWER") | 0.4,
                "empty_choice": os.getenv("PENALTY_EMPTY_CHOICE") | 0.1,
                "duplicated_choices": os.getenv("PENALTY_DUPLICATED_CHOICES") | 0.1,
                "grammar_error": os.getenv("PENALTY_GRAMMAR_ERROR") | 0.05
            }
        },
        "distractor": {
            "empty_choice_deduction":  os.getenv("DISTRACTOR_EMPTY_CHOICE_DEDUCTION") | 0.05,       # trong _check_pos_and_meaning_of_choice
            "embedding_similarity_thresholds": {
                "too_different":  os.getenv("DISTRACTOR_EMBEDDING_SIMILARITY_TOO_DIFFERENT") |0.35,
                "moderate":  os.getenv("DISTRACTOR_EMBEDDING_SIMILARITY_MODERATE") |0.45,
                "good":  os.getenv("DISTRACTOR_EMBEDDING_SIMILARITY_GOOD") |0.6,
                "strong":  os.getenv("DISTRACTOR_EMBEDDING_SIMILARITY_STRONG") |0.7
            },
            "paragraph":  {
                "length_weight":  os.getenv("DISTRACTOR_PARAGRAPH_LENGTH_WEIGHT") |0.1,
                "difficulty_weight":  os.getenv("DISTRACTOR_PARAGRAPH_DIFFICULTY_WEIGHT") |0.9,
                "vocab_length_thresholds":  os.getenv("DISTRACTOR_PARAGRAPH_VOCAB_LENGTH_THRESHOLDS") |[50, 100, 200, 300],  # tương ứng score 0.2 → 0.5
                "other_length_thresholds":  os.getenv("DISTRACTOR_PARAGRAPH_OTHER_LENGTH_THRESHOLDS") |[50, 100, 200, 300],  # tương ứng 0.3 → 1.0
                "direct_match_sim":  os.getenv("DISTRACTOR_PARAGRAPH_DIRECT_MATCH_SIM") |0.85,
                "paraphrase_sim":  os.getenv("DISTRACTOR_PARAGRAPH_PARAPHRASE_SIM") |0.5,
                "difficulty_levels":  os.getenv("DISTRACTOR_PARAGRAPH_DIFFICULTY_LEVELS") |[1, 3, 5]  
            },
            "lexical_family":  {
                "thresholds":  {
                    "high_lemma":  os.getenv("DISTRACTOR_LEXICAL_FAMILY_HIGH_LEMMA") |0.9,
                    "high_pos":  os.getenv("DISTRACTOR_LEXICAL_FAMILY_HIGH_POS") |0.9,
                    "medium_high_pos":  os.getenv("DISTRACTOR_LEXICAL_FAMILY_MEDIUM_HIGH_POS") |0.6,
                    "medium_lemma":  os.getenv("DISTRACTOR_LEXICAL_FAMILY_MEDIUM_LEMMA") |0.7,
                    "medium_both":  os.getenv("DISTRACTOR_LEXICAL_FAMILY_MEDIUM_BOTH") |0.4,
                    "low":  os.getenv("DISTRACTOR_LEXICAL_FAMILY_LOW") |0.3
                },
                "scores":  {
                    "high_lemma":  os.getenv("DISTRACTOR_LEXICAL_FAMILY_HIGH_LEMMA_SCORE") |0.75,
                    "high_pos":  os.getenv("DISTRACTOR_LEXICAL_FAMILY_HIGH_POS_SCORE") |0.9,
                    "medium_high_pos":  os.getenv("DISTRACTOR_LEXICAL_FAMILY_MEDIUM_HIGH_POS_SCORE") |0.7,
                    "medium_lemma":  os.getenv("DISTRACTOR_LEXICAL_FAMILY_MEDIUM_LEMMA_SCORE") |0.6,
                    "medium_both":  os.getenv("DISTRACTOR_LEXICAL_FAMILY_MEDIUM_BOTH_SCORE") |0.45,
                    "low":  os.getenv("DISTRACTOR_LEXICAL_FAMILY_LOW_SCORE") |0.3
                }
            }
        }
    }

}