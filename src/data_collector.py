import pandas as pd
import random
import uuid
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import genai

class DataCollector:
    def __init__(self, topic="Yapay Zeka"):
        self.topic = topic
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.users = ["user123", "cool_boy", "tech_savy", "ayse_yilmaz", "mehmet_b", "john_doe", "ai_lover", "skeptic_guy"]
    
    def _get_fallback_mock_data(self, count):
        """Fallback mock data if API fails or no key."""
        # ... (Same fallback data as before) ...
        mock_templates = [
            f"{self.topic} dünyayı değiştirecek! #AI #Gelecek",
            f"{self.topic} hakkında harika bir makale okudum.",
            f"Bence {self.topic} biraz abartılıyor. #balon",
            f"{self.topic} ile ödevlerimi yapıyorum, çok kolaylaştı.",
            f"Bugünlük {self.topic} dozumuzu aldık. İnanılmaz gelişmeler var.",
            "Yapay zeka işleri elimizden alacak mı?",
            "AI is shaping the future of humanity.",
            "Just tried a new AI tool, mind blowing!",
            "I'm skeptical about the ethics of AI.",
            "Machine learning is specifically fascinating."
        ]
        return [random.choice(mock_templates) for _ in range(count)]

    def _generate_with_gemini(self, count):
        """Generates realistic tweets using Google Gemini API (New SDK)."""
        if not self.api_key:
            return None

        try:
            client = genai.Client(api_key=self.api_key)
            
            prompt = f"""
            You are a social media data generator. Generate {count} unique, realistic tweets/posts about "{self.topic}".
            
            Rules:
            1. Mix of Turkish and English.
            2. Vary the sentiment (positive, negative, neutral).
            3. Include some "noise" like typos, slang, hashtags, and URLs.
            4. Make them look like real user opinions, news, or complaints.
            5. Return ONLY the raw texts, separated by a pipe character (|). Do not number them.
            
            Example output format:
            This is a tweet|Another one here|Yapay zeka harika!
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            
            if response.text:
                tweets = response.text.split('|')
                tweets = [t.strip() for t in tweets if t.strip()]
                return tweets
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return None
        return None

    def generate_data(self, count=50):
        data = []
        
        # Try fetching real generative data
        texts = self._generate_with_gemini(count)
        
        if not texts or len(texts) < count:
            # Output info only if falling back
            if not texts:
                texts = []
            remaining = count - len(texts)
            if remaining > 0:
                texts.extend(self._get_fallback_mock_data(remaining))
        
        texts = texts[:count]

        for text in texts:
            # Simulate date
            days_back = random.randint(0, 30)
            date = datetime.now() - timedelta(days=days_back, minutes=random.randint(0, 1440))
            
            record = {
                "id": str(uuid.uuid4()),
                "text": text,
                "user": random.choice(self.users),
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "platform": random.choice(["Twitter", "Instagram", "LinkedIn"])
            }
            data.append(record)
            
        return pd.DataFrame(data)

if __name__ == "__main__":
    dc = DataCollector()
    df = dc.generate_data(5)
    print(df)
