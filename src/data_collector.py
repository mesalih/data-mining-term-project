import pandas as pd
import random
from datetime import datetime, timedelta
import uuid
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DataCollector:
    def __init__(self, topic="Yapay Zeka"):
        self.topic = topic
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.users = ["user123", "cool_boy", "tech_savy", "ayse_yilmaz", "mehmet_b", "john_doe", "ai_lover", "skeptic_guy"]
    
    def _generate_with_gemini(self, count):
        """
        Uses Gemini API to generate realistic tweets.
        """
        if not self.api_key:
            print("⚠️ No API Key found. Falling back to simple mock data.")
            return None

        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
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
            
            response = model.generate_content(prompt)
            if response.text:
                tweets = response.text.split('|')
                # Clean up any potential whitespace around split
                tweets = [t.strip() for t in tweets if t.strip()]
                return tweets
            
        except Exception as e:
            print(f"⚠️ Gemini API Error: {e}")
            return None
        
        return None

    def _get_fallback_mock_data(self, count):
        """
        Fallback mock templates if API fails.
        """
        templates = [
            "Yapay zeka geleceği ele geçirecek mi? 🤖 #AI #Future",
            "I love how AI is changing our daily lives! So efficient.",
            "ChatGPT yine hata verdi, inanılmaz sinir bozucu... 😡",
            "Yapay zeka işlerimizi elimizden alacak, çok korkuyorum.",
            "New AI tools are just amazing for productivity. 🚀",
            "Bu yapay zeka mevzusu çok abartılıyor bence.",
            "AI generated art is not real art! #Sanat",
            "Yapay zeka sayesinde ödevlerimi 5 dakikada bitirdim :D",
            "Privacy concerns with AI are growing everyday. https://example.com/news",
            "Yapay zeka ve etik konuları üzerine uzun bir yazı yazdım: www.blog.com",
            "Hahaha AI çok komik cevaplar veriyor bazen 😂",
            "Teknoloji devi X şirketi yeni AI modelini duyurdu.",
            "Yapay zaka yüzünden yazılımcılar işsiz kalacak mı? (Typo intentional)",
            "AI is dangerous if not regulated properly!!!",
            "Harika bir gelişme! Tıp alanında yapay zeka devrimi.",
            "Sıkıcı bir gün, yapay zeka ile sohbet ediyorum.",
            "RT @TechGuru: The best AI tool of 2024 is here!",
            "Yapay zeka dersi çok zor, hiçbir şey anlamadım :(",
            "AI?? More like Artificial Stupidity lol",
            "Gelecek yapay zekada. Yatırım tavsiyesidir."
        ]
        return [random.choice(templates) for _ in range(count)]

    def generate_data(self, count=100):
        data = []
        
        # Try Gemini first
        texts = self._generate_with_gemini(count)
        
        # Fallback if needed
        if not texts or len(texts) < count:
            if not texts:
                texts = []
            remaining = count - len(texts)
            if remaining > 0:
                texts.extend(self._get_fallback_mock_data(remaining))
        
        # Trim if we got too many
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
    collector = DataCollector()
    df = collector.generate_data(5)
    print(df.head())
