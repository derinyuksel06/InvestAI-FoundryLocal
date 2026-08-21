# InvestAI

InvestAI is a local investment education assistant built with Microsoft Foundry Local.

It uses Retrieval-Augmented Generation (RAG) to search trusted local investment sources before generating an answer.

## Features

- Runs locally with Microsoft Foundry Local
- Semantic search with sentence embeddings
- Source-grounded answers
- Refuses unsupported questions
- Refuses personalised investment advice
- Refuses future price predictions
- Streamlit web interface

## Knowledge Base

- Investing basics
- ETFs
- Diversification
- Financial statements
- 10-K reports
- Bonds
- Fund fees and expenses
- Compound interest
- Risk Factors and MD&A

## Evaluation

InvestAI was tested on a 20-question evaluation set.

- Retrieval Accuracy: 100% (14/14)
- Refusal Accuracy: 100% (6/6)
- Overall Evaluation: 100% (20/20)

These results apply only to the current curated evaluation set.

## How to Run

Build the index:

```bash
python src/build_index.py