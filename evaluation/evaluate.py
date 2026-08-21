import sys
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from src.query import (
    retrieve,
    SIMILARITY_THRESHOLD,
    requires_safety_refusal,
)


QUESTIONS_PATH = BASE_DIR / "evaluation" / "questions.json"


def load_questions():

    with open(
        QUESTIONS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    questions = load_questions()

    retrieval_correct = 0
    retrieval_tests = 0

    refusal_correct = 0
    refusal_tests = 0

    failures = []

    print("\n====================================")
    print("        InvestAI Evaluation")
    print("====================================\n")

    for number, item in enumerate(
        questions,
        start=1
    ):

        question = item["question"]
        expected_source = item["expected_source"]
        should_refuse = item["should_refuse"]

        retrieved_chunks = retrieve(
            question,
            top_k=3
        )

        best_score = retrieved_chunks[0]["score"]

        retrieved_sources = [
            chunk["source"]
            for chunk in retrieved_chunks
        ]

        safety_refusal = requires_safety_refusal(
            question
        )

        similarity_refusal = (
            best_score
            < SIMILARITY_THRESHOLD
        )

        predicted_refusal = (
            safety_refusal
            or similarity_refusal
        )

        print(
            f"[{number}/{len(questions)}] "
            f"{question}"
        )

        print(
            f"Best score: {best_score:.3f}"
        )

        print(
            f"Safety refusal: {safety_refusal}"
        )

        # ==========================================
        # REFUSAL TEST
        # ==========================================

        if should_refuse:

            refusal_tests += 1

            if predicted_refusal:

                refusal_correct += 1

                print(
                    "✅ Correct refusal"
                )

            else:

                print(
                    "❌ Should have refused"
                )

                failures.append(
                    {
                        "type": "REFUSAL",
                        "question": question,
                        "score": best_score,
                        "expected": "REFUSE",
                        "retrieved": retrieved_sources
                    }
                )

        # ==========================================
        # RETRIEVAL TEST
        # ==========================================

        else:

            retrieval_tests += 1

            if expected_source in retrieved_sources:

                retrieval_correct += 1

                print(
                    "✅ Correct source retrieved"
                )

            else:

                print(
                    "❌ Expected source missing"
                )

                failures.append(
                    {
                        "type": "RETRIEVAL",
                        "question": question,
                        "score": best_score,
                        "expected": expected_source,
                        "retrieved": retrieved_sources
                    }
                )

        print("-" * 60)


    retrieval_accuracy = (
        retrieval_correct
        / retrieval_tests
        * 100
    )

    refusal_accuracy = (
        refusal_correct
        / refusal_tests
        * 100
    )

    overall_correct = (
        retrieval_correct
        + refusal_correct
    )

    total_tests = len(questions)

    overall_accuracy = (
        overall_correct
        / total_tests
        * 100
    )


    print("\n====================================")
    print("              RESULTS")
    print("====================================")

    print(
        f"\nRetrieval Accuracy: "
        f"{retrieval_accuracy:.1f}% "
        f"({retrieval_correct}/{retrieval_tests})"
    )

    print(
        f"Refusal Accuracy: "
        f"{refusal_accuracy:.1f}% "
        f"({refusal_correct}/{refusal_tests})"
    )

    print(
        f"Overall Evaluation: "
        f"{overall_accuracy:.1f}%"
    )

    print(
        f"Correct Tests: "
        f"{overall_correct}/{total_tests}"
    )


    print("\n====================================")
    print("           FAILED TESTS")
    print("====================================\n")

    if not failures:

        print(
            "🎉 No failed tests!"
        )

    else:

        for number, failure in enumerate(
            failures,
            start=1
        ):

            print(
                f"FAIL {number}"
            )

            print(
                f"Type: {failure['type']}"
            )

            print(
                f"Question: {failure['question']}"
            )

            print(
                f"Best score: {failure['score']:.3f}"
            )

            print(
                f"Expected: {failure['expected']}"
            )

            print(
                "Retrieved:"
            )

            for source in failure["retrieved"]:

                print(
                    f"  - {source}"
                )

            print(
                "-" * 60
            )


if __name__ == "__main__":
    main()