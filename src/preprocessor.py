import re
import string
import nltk

# Download necessary NLTK data (safe to run multiple times, checks first)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

class Preprocessor:
    def __init__(self):
        self.stop_words_tr = set(stopwords.words('turkish'))
        self.stop_words_en = set(stopwords.words('english'))
        # Using English stemmer as a fallback/demo since Turkish stemmers in NLTK are limited/non-existent
        # Ideally would use Zemberek for Turkish, but that requires Java/heavy setup. 
        # Using a simple custom suffix stripper for Turkish demo purposes if needed, 
        # but for now we'll stick to basic normalization and English stemming for mixed content.
        self.stemmer = SnowballStemmer("english")

    def clean_text(self, text):
        """
        Removes URLs, mentions, hashtags, and special characters.
        """
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove mentions (@user)
        text = re.sub(r'@\w+', '', text)
        # Remove hashtags (#tag) - optionally keep the text inside
        text = re.sub(r'#\w+', '', text) 
        # Remove punctuation and numbers
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        return text

    def normalize_text(self, text):
        """
        Converts to lowercase and removes stopwords.
        """
        text = text.lower()
        tokens = text.split() # Simple whitespace tokenizer
        
        # Remove stopwords (checking both TR and EN lists)
        tokens = [t for t in tokens if t not in self.stop_words_tr and t not in self.stop_words_en]
        
        return " ".join(tokens)

    def stem_text(self, text):
        """
        Applies stemming to words.
        """
        tokens = text.split()
        stemmed_tokens = [self.stemmer.stem(t) for t in tokens]
        return " ".join(stemmed_tokens)

    def process(self, text):
        """
        Full preprocessing pipeline.
        """
        cleaned = self.clean_text(text)
        normalized = self.normalize_text(cleaned)
        stemmed = self.stem_text(normalized)
        return stemmed

if __name__ == "__main__":
    p = Preprocessor()
    sample = "Yapay zeka geleceği ele geçirecek mi? Check this out: http://test.com"
    print(f"Original: {sample}")
    print(f"Processed: {p.process(sample)}")
