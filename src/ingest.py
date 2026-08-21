from pathlib import Path


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# ==================================================
# CHUNK TEXT
# ==================================================

def chunk_text(text, chunk_size=900, overlap=150):

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0
    chunk_id = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:

            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": chunk
                }
            )

            chunk_id += 1

        if end >= len(text):
            break

        start = end - overlap

    return chunks


# ==================================================
# LOAD ALL TXT DOCUMENTS
# ==================================================

def load_documents():

    all_chunks = []

    files = sorted(
        DATA_DIR.glob("*.txt")
    )

    print(
        f"Found {len(files)} source files."
    )

    for file_path in files:

        print(
            f"Loading: {file_path.name}"
        )

        text = file_path.read_text(
            encoding="utf-8"
        )

        chunks = chunk_text(text)

        for chunk in chunks:

            all_chunks.append(
                {
                    "source": file_path.name,
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"]
                }
            )

    return all_chunks


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    chunks = load_documents()

    print(
        f"\nLoaded {len(chunks)} chunks.\n"
    )

    for chunk in chunks:

        print(
            f"SOURCE: {chunk['source']} | "
            f"CHUNK: {chunk['chunk_id']}"
        )

        print(
            chunk["text"]
        )

        print(
            "-" * 70
        )