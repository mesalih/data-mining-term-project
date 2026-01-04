from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd

class SentimentAnalyzer:
    def __init__(self):
        # Using a pipeline to combine vectorization and classification
        self.model = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', MultinomialNB())
        ])
        self.is_trained = False

    def train_mock_model(self):
        """
        Trains the model on a small hardcoded dataset for demonstration purposes.
        In a real scenario, this would load a large labeled CSV.
        """
        # Small labeled dataset (mixed TR/EN)
        data = [
            ("I love this product", "Positive"),
            ("Harika bir deneyim", "Positive"),
            ("This is the worst service ever", "Negative"),
            ("Berbat bir durum", "Negative"),
            ("It is okay, nothing special", "Neutral"),
            ("Fena değil, idare eder", "Neutral"),
            ("Amazing quality and fast delivery", "Positive"),
            ("Çok hızlı geldi teşekkürler", "Positive"),
            ("I hate waiting so long", "Negative"),
            ("Hiç beğenmedim, iade ettim", "Negative"),
            ("Just a regular day", "Neutral"),
            ("Sıradan bir ürün", "Neutral"),
            ("Yapay zeka çok heyecan verici", "Positive"),
            ("AI is scary and dangerous", "Negative"),
            ("The weather is nice today", "Neutral"),
            ("Bugün hava güzel", "Neutral")
        ]
        
        df = pd.DataFrame(data, columns=["text", "sentiment"])
        X = df["text"]
        y = df["sentiment"]
        
        self.model.fit(X, y)
        self.is_trained = True
        print("Model trained on mock dataset.")

    def predict(self, text):
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        
        return self.model.predict([text])[0]

    def predict_batch(self, texts):
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        return self.model.predict(texts)

if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    analyzer.train_mock_model()
    print(analyzer.predict("Bu çok kötü bir deneyimdi"))
    print(analyzer.predict("I am so happy with this"))
