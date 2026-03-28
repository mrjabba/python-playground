import matplotlib.pyplot as plt         # for displaying data
from wordcloud import WordCloud
from datasets import load_dataset

"""
This script creates a visual word cloud from Star Trek Spock dialogue data. 
It aggregates all dialogues from the Spock dataset and generates a frequency-based visualization 
where the most common words appear larger.
"""
# Load the Spock dataset from Hugging Face
dataset = load_dataset("omgbobbyg/spock")
dialogues = dataset['train']['dialogue']  # Get all dialogues from training set

# Combine all dialogues into one string
text = " ".join(dialogues)

# Generate a word cloud image
wordcloud = WordCloud(max_font_size=60).generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()