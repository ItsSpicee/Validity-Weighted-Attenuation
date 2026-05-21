"""
constants.py
------------
Single source for all configuration values, file paths,
hyperparameters, and domain definitions used across the framework.
"""

from pathlib import Path

# ==============================================================================
# PATHS
# ==============================================================================

DATA_DIR   = Path("data")
MODELS_DIR = Path("models")

# Inputs
RAW_DATASET        = DATA_DIR / "raw" / "RateMyProfessor_Sample data.csv"

# Intermediate outputs (written and read between stages)
PROFESSORS_CLEANED = DATA_DIR / "processed" / "professors_cleaned.csv"
REVIEWS_CLEANED    = DATA_DIR / "processed" / "reviews_cleaned.csv"
REVIEWS_TEXT       = DATA_DIR / "processed" / "reviews_text_cleaned.csv"
CLAUSE_DATASET     = DATA_DIR / "processed" / "clause_dataset.csv"
EXPLODED_CLAUSES   = DATA_DIR / "processed" / "exploded_clauses.csv"
ATC_EXTRACTED      = DATA_DIR / "processed" / "ATExtracted_reviews.csv"
CLAUSE_VECTORS     = DATA_DIR / "processed" / "final_clause_vectors.parquet"
FINAL_EMOTIONS     = DATA_DIR / "processed" / "final_emotions.csv"
WEIGHTED_EMOTIONS  = DATA_DIR / "processed" / "weighted_emotions.csv"

# Final outputs
ATTUNED_RATINGS      = DATA_DIR / "processed" / "attuned_ratings.csv"
ATTUNED_RATINGS_FULL = DATA_DIR / "processed" / "attuned_ratings_full.csv"

# Models
CATBOOST_MODEL       = MODELS_DIR / "cat_boost.cbm"
CATBOOST_FINAL_MODEL = MODELS_DIR / "cat_boost_final.cbm"
FEATURE_IMPORTANCE   = MODELS_DIR / "final_feature_importance.csv"


# ==============================================================================
# PREPROCESSING
# ==============================================================================

MIN_REVIEWS_PER_PROF = 8

# ==============================================================================
# ATC (Aspect Term Categorization)
# ==============================================================================

SIMILARITY_THRESHOLD = 0.25
EMBEDDING_MODEL      = "sentence-transformers/all-mpnet-base-v2"

TOPIC_DESCRIPTIONS = {
    "instructional_effectiveness": {
        "descriptions": [
            "clear and effective explanations of concepts and material",
            "makes difficult topics understandable with good examples or structure",
            "lectures are well-organized, logical, and easy to follow",
            "helps students learn and grasp the subject matter successfully",
            "I've learned a lot / learned more useful stuff than in other classes",
            "very knowledgeable about the topic and conveys it well",
            "provides helpful clarification when students don't understand",
            "answers questions, reteaches concepts, or explains in different ways",
            "always willing to help students understand the content",
            "works with different learning styles to make material accessible",
            "devoted to teaching and making the subject engaging through delivery",
            "educational, interesting, or makes the class intellectually valuable",
            "clear and organized lectures/assignments that aid studying and learning",
        ]
    },
    "fairness": {
        "descriptions": [
            "grading feels fair, earned, and based on actual performance",
            "tough but fair grader, very detailed and consistent evaluation",
            "grades by skill level or progress rather than strict letter grades",
            "adjusts grading to student's current ability or advancement",
            "drops lowest scores or has reasonable grading accommodations",
            "lenient, understanding, or kind-hearted in grading policies",
            "tough grading or strict rules but ultimately fair and preparatory",
            "grade based purely on number of tests, assignments, or clear criteria",
        ]
    },
    "workload": {
        "descriptions": [
            "heavy workload, lots of effort and time required to succeed",
            "very stressful, requires many hours per week on homework/assignments",
            "tests, exams, labs, or quizzes are hard or demanding",
            "easy class, light workload, assignments are very easy",
            "sections or tasks feel easy but pointless or minimal",
            "just show up, pay attention, take notes and you'll be fine",
            "easy exams if you study basic materials like powerpoints",
            "do the packets, board work, assigned readings, or simple daily tasks",
            "specific assignments like vlogs, research papers, major papers required",
            "no textbook, only assigned readings or light materials",
            "must attend class or do basic work to pass / low attendance penalty",
            "didn't go to class much and still passed / low effort to decent grade",
            "intense finals or content that requires knowing everything",
        ]
    },
}


TOPICS = list(TOPIC_DESCRIPTIONS.keys()) + ["misc"]

TOPIC_DISPLAY_NAMES = {
    "instructional_effectiveness": "Instructional\nEffectiveness",
    "workload":                    "Workload",
    "fairness":                    "Fairness",
    "misc":                        "Miscellaneous",
}

# ==============================================================================
# SENTIMENT (RoBERTa GoEmotions)
# ==============================================================================

ROBERTA_MODEL_REPO = "SamLowe/roberta-base-go_emotions-onnx"
ROBERTA_MODEL_FILE = "onnx/model_quantized.onnx"
ROBERTA_TOKENIZER  = "SamLowe/roberta-base-go_emotions"

EMOTION_LABELS = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring",
    "confusion", "curiosity", "desire", "disappointment", "disapproval",
    "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
    "joy", "love", "nervousness", "optimism", "pride", "realization",
    "relief", "remorse", "sadness", "surprise", "neutral",
]

# Neutral is excluded from downstream modelling
EMOTION_LABELS_NO_NEUTRAL = [e for e in EMOTION_LABELS if e != "neutral"]

POS_EMOTIONS = {
    "admiration", "amusement", "approval", "caring", "desire",
    "excitement", "gratitude", "joy", "love", "optimism",
    "pride", "relief", "curiosity", "realization",
}
NEG_EMOTIONS = {
    "anger", "annoyance", "disappointment", "disapproval",
    "disgust", "embarrassment", "fear", "grief",
    "nervousness", "remorse", "sadness", "confusion",
}

# ==============================================================================
# REGRESSION (CatBoost)
# ==============================================================================

METADATA_COLS = ["review_id", "prof_ID", "rating"]

CATBOOST_PARAMS = {
    "iterations":            1000,
    "learning_rate":         0.02,
    "depth":                 7,
    "l2_leaf_reg":           6,
    "loss_function":         "MAE",
    "eval_metric":           "MAE",
    "early_stopping_rounds": 50,
    "verbose":               100,
}

CV_N_SPLITS  = 5
TEST_SIZE    = 0.2
RANDOM_STATE = 42

# ==============================================================================
# ATTENUATION
# ==============================================================================

S_VALUE = 0.86          # optimal down_weighting exponent 
MISC_D_COL = "misc_d"

# S optimization grid search range
S_SEARCH_MIN  = 0.2
S_SEARCH_MAX  = 1.0
S_SEARCH_STEP = 0.01

# Composite loss weights
ALPHA  = 175.0   # pedagogical reward weight
BETA   = 2.0     # misc leakage penalty weight
DELTA  = 1    # alignment reward weight
LAMBDA = 0.01    # hinge tolerance for small pedagogical correlation drops



# ==============================================================================
# VALIDATION
# ==============================================================================

COARSE_DELTA_THRESHOLD   = 0.5
FINE_DELTA_MIN           = 0
FINE_DELTA_MAX           = 0.4

EXPERT_LABELS_PATH   = DATA_DIR / "raw" / "expert_labels.csv"


# ATC validation
ATC_EXPERT_LABELS        = DATA_DIR / "raw" / "atc_expert_labels.xlsx"
ATC_PREDICTIONS          = DATA_DIR / "raw" / "atc_predictions.csv"
GROK_LABELS              = DATA_DIR / "raw" / "grok.csv"
GPT_LABELS               = DATA_DIR / "raw" / "gpt.csv"
