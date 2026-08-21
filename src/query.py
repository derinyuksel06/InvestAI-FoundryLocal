from pathlib import Path
import json

import numpy as np
from sentence_transformers import SentenceTransformer

from foundry_local_sdk import (
    FoundryLocalManager,
    Configuration,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_DIR = BASE_DIR / "index"

EMBEDDINGS_PATH = INDEX_DIR / "embeddings.npy"
METADATA_PATH = INDEX_DIR / "metadata.json"


# ============================================================
# SETTINGS
# ============================================================

SIMILARITY_THRESHOLD = 0.30

REFUSAL_MESSAGE = (
    "I don't have enough information in my trusted sources "
    "to answer that."
)

ADVICE_REFUSAL_MESSAGE = (
    "I can explain investment concepts, risks, and educational "
    "information, but I can't provide personalised investment "
    "recommendations or predict future prices."
)


# ============================================================
# SAFETY GUARDRAIL
# ============================================================

def requires_safety_refusal(question):

    question = question.lower().strip()

    blocked_phrases = [
        "should i buy",
        "should i sell",
        "should i invest",
        "should i put",
        "should i put all",
        "should i put my",
        "what should i buy",
        "what stock should i buy",
        "which stock should i buy",
        "which crypto should i buy",
        "which cryptocurrency should i buy",
        "where should i invest",
        "all my savings",
        "my savings into",
        "what will bitcoin cost",
        "what will bitcoin",
        "will bitcoin cost",
        "share price be",
        "stock price be",
        "price next year",
        "price next month",
    ]

    return any(
        phrase in question
        for phrase in blocked_phrases
    )


# ============================================================
# LOAD RETRIEVAL DATA
# ============================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

document_embeddings = np.load(
    EMBEDDINGS_PATH
)

with open(
    METADATA_PATH,
    "r",
    encoding="utf-8"
) as file:

    metadata = json.load(file)


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve(question, top_k=3):

    question_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True
    )[0]

    scores = np.dot(
        document_embeddings,
        question_embedding
    )

    top_indices = np.argsort(
        scores
    )[::-1][:top_k]

    results = []

    for index in top_indices:

        chunk = metadata[index].copy()

        chunk["score"] = float(
            scores[index]
        )

        results.append(
            chunk
        )

    return results


# ============================================================
# SOURCE LIST
# ============================================================

def get_unique_sources(retrieved_chunks):

    sources = []

    for chunk in retrieved_chunks:

        source = chunk["source"]

        if source not in sources:

            sources.append(
                source
            )

    return sources


# ============================================================
# FOUNDRY LOCAL
# ============================================================

_manager = None
_chat_model = None
_client = None


def get_chat_client():

    global _manager
    global _chat_model
    global _client

    if _client is not None:
        return _client

    try:

        FoundryLocalManager.initialize(
            Configuration(
                app_name="InvestAI"
            )
        )

    except Exception as error:

        # FoundryLocalManager is a singleton.
        # If already initialized, continue using it.
        if "already been initialized" not in str(error):
            raise

    _manager = FoundryLocalManager.instance

    _chat_model = _manager.catalog.get_model(
        "qwen3-1.7b"
    )

    _chat_model.download()
    _chat_model.load()

    _client = _chat_model.get_chat_client()

    return _client


# ============================================================
# REMOVE QWEN THINKING OUTPUT
# ============================================================

def clean_answer(answer):

    if not answer:
        return ""

    if "</think>" in answer:

        answer = answer.split(
            "</think>",
            1
        )[1]

    return answer.strip()


# ============================================================
# GENERATE GROUNDED ANSWER
# ============================================================

def generate_answer(
    question,
    retrieved_chunks
):

    client = get_chat_client()

    context_parts = []

    for chunk in retrieved_chunks:

        context_parts.append(
            f"""
SOURCE: {chunk['source']}

{chunk['text']}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = f"""
You are InvestAI, an educational investment research assistant.

RULES:

1. Answer using ONLY the trusted context below.

2. Do not invent facts that are not supported by the context.

3. Do not provide personalised financial advice.

4. Do not predict future stock, cryptocurrency, or asset prices.

5. If the context does not contain enough information to answer,
reply exactly:

{REFUSAL_MESSAGE}

6. Keep the answer clear, concise, and beginner-friendly.

7. Do not create a Sources section.
The application will show sources separately.


TRUSTED CONTEXT:

{context}


QUESTION:

{question}


ANSWER:
"""

    response = client.complete_chat(
        [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = (
        response
        .choices[0]
        .message
        .content
    )

    return clean_answer(
        answer
    )


# ============================================================
# ONE FUNCTION FOR THE WHOLE APPLICATION
# ============================================================

def ask_investai(question):

    # Safety check FIRST

    if requires_safety_refusal(
        question
    ):

        return {
            "answer": ADVICE_REFUSAL_MESSAGE,
            "sources": [],
            "score": None,
            "refused": True,
            "reason": "safety"
        }


    # Retrieval

    retrieved_chunks = retrieve(
        question,
        top_k=3
    )

    best_score = retrieved_chunks[0][
        "score"
    ]


    # Knowledge boundary

    if (
        best_score
        < SIMILARITY_THRESHOLD
    ):

        return {
            "answer": REFUSAL_MESSAGE,
            "sources": [],
            "score": best_score,
            "refused": True,
            "reason": "low_similarity"
        }


    # Grounded generation

    answer = generate_answer(
        question,
        retrieved_chunks
    )

    sources = get_unique_sources(
        retrieved_chunks
    )

    return {
        "answer": answer,
        "sources": sources,
        "score": best_score,
        "refused": False,
        "reason": None
    }