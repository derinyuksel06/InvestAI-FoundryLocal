import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from ingest import load_documents


BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_DIR = BASE_DIR / "index"

INDEX_DIR.mkdir(exist_ok=True)

EMBEDDINGS_PATH = INDEX_DIR / "embeddings.npy"
METADATA_PATH = INDEX_DIR / "metadata.json"


def build_index():
    print("Loading documents...")

    chunks = load_documents()

    texts = [chunk["text"] for chunk in chunks]

    print(f"Loaded {len(chunks)} chunks.")
    print("Creating embeddings...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    np.save(EMBEDDINGS_PATH, embeddings)

    with open(METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)

    print("\nIndex built successfully.")
    print(f"Embeddings saved to: {EMBEDDINGS_PATH}")
    print(f"Metadata saved to: {METADATA_PATH}")
    print(f"Embedding shape: {embeddings.shape}")


if __name__ == "__main__":
    build_index()