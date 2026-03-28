from datasets import load_dataset
from transformers import pipeline
"""
This script analyzes the sentiment of Reddit soccer comments using pre-trained deep learning models from Hugging Face. 
It loads a public Reddit soccer dataset, filters for valid comments, and classifies each comment as positive or negative using DistilBERT.
Another experiment with sentiment analysis.
"""
def is_valid_comment(x):
    c = x["comment"]
    return isinstance(c, str) and len(c.strip()) > 0

def main():
    dataset = load_dataset("singhala/reddit_soccer")
    train = dataset["train"]

    # Strong filter
    train = train.filter(is_valid_comment)

    sentiment_pipe = pipeline(
        "text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

    sample = train.select(range(10))

    # Defensive conversion
    texts = [str(t) for t in sample["comment"]]

    results = sentiment_pipe(texts)

    for text, res in zip(texts, results):
        print("TEXT:", text[:120].replace("\n", " "), "...")
        print("SENTIMENT:", res["label"], "SCORE:", round(res["score"], 3))
        print("-" * 60)

if __name__ == "__main__":
    main()
