import os
from collections import Counter
import string
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def clean_text(text):
    # Remove punctuation and make lowercase
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator).lower()

def get_word_frequencies(filenames, exclude_words):
    word_counter = Counter()

    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
            cleaned_text = clean_text(text)
            words = cleaned_text.split()
            # Filter out excluded words
            filtered_words = [word for word in words if word not in exclude_words]
            word_counter.update(filtered_words)

    return word_counter

# List of file names
filenames = [f'gemini/s{i}.txt' for i in range(1, 9)]

# List of words to exclude (common articles and conjunctions)
exclude_words = {'a', 'an', 'the', 'and', 'or', 'in', 'on', 'with', 'of', 'at', 'by', 'for', 'to', 'as', 'is'}

# Get word frequencies excluding the articles and conjunctions
word_frequencies = get_word_frequencies(filenames, exclude_words)

# Get the top 50 most frequent words
top_50 = word_frequencies.most_common(50)

# Save the top 50 words and frequencies to a CSV file
df = pd.DataFrame(top_50, columns=['Word', 'Frequency'])
df.to_csv('claude_top_50_words.csv', index=False)
print("Top 50 words saved to 'top_50_words.csv'.")

# Generate a word cloud from keywords
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(top_50))

# Save the word cloud image
wordcloud.to_file('claude_wordcloud.png')
print("Word cloud saved as 'wordcloud.png'.")

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
