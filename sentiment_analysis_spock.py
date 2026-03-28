import os
from datasets import load_dataset
from transformers import pipeline

"""
This script performs sentiment analysis on Star Trek Spock dialogue data. 
It loads dialogues from a Hugging Face dataset, classifies the sentiment of each dialogue using DistilBERT, 
and provides a summary breakdown of positive vs. negative sentiments.
"""

# Ensure token is set
if not os.environ.get('HF_TOKEN'):
    token_path = os.path.expanduser('~/.huggingface/token')
    if os.path.exists(token_path):
        with open(token_path, 'r') as f:
            os.environ['HF_TOKEN'] = f.read().strip()

# Load the Spock dataset from Hugging Face
dataset = load_dataset("omgbobbyg/spock")
dialogues = dataset['train']['dialogue']

# Create a sentiment analysis pipeline with explicit model
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"
)

# Analyze sentiment for each dialogue
print("Analyzing sentiment for dialogues...\n")
sentiments = []
for i, dialogue in enumerate(dialogues[:10]):  # Limit to first 10 for demo
    result = sentiment_pipeline(dialogue[:512])  # Limit to 512 chars (model limit)
    sentiments.append(result[0])
    print(f"Dialogue {i}: {dialogue[:100]}...")
    print(f"Sentiment: {result[0]['label']} (confidence: {result[0]['score']:.2f})\n")

# Summary of results
print("\n=== Summary ===")
positive = sum(1 for s in sentiments if s['label'] == 'POSITIVE')
negative = sum(1 for s in sentiments if s['label'] == 'NEGATIVE')
print(f"Positive: {positive}")
print(f"Negative: {negative}")
