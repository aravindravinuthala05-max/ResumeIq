"""Explicit one-time provisioning for ResumeIQ's local semantic model.

Run this script only in a controlled environment with network access. Runtime
loading in semantic_matcher.py remains cache-only and never downloads models.
"""

import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from semantic_matcher import MODEL_NAME


def main():
    print(f"Provisioning {MODEL_NAME} into the standard Hugging Face cache...")
    SentenceTransformer(MODEL_NAME)
    model = SentenceTransformer(MODEL_NAME, local_files_only=True)
    embeddings = model.encode(
        ["data analysis and numerical computing", "Built data pipelines using pandas and NumPy."],
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    print(f"Provisioned locally; embedding shape: {tuple(embeddings.shape)}")


if __name__ == "__main__":
    main()
