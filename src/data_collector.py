import pandas as pd
import random
import uuid
import os
import requests
import zipfile
import shutil
from datetime import datetime, timedelta
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

class DataCollector:
    def __init__(self, topic="Yapay Zeka"):
        self.topic = topic
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.zip_path = os.path.join(self.data_dir, "tweets.zip")
        self.csv_path = os.path.join(self.data_dir, "tweets.csv")
        self.repo_url = "https://github.com/ezgisubasi/turkish-tweets-sentiment-analysis/archive/refs/heads/master.zip"
        self.users = ["user123", "cool_boy", "tech_savy", "ayse_yilmaz", "mehmet_b", "john_doe", "ai_lover", "skeptic_guy"]
        
        # Ensure data directory exists
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _download_and_extract_if_needed(self):
        """Downloads and extracts the dataset if not present."""
        
        # 1. Check if tweets.csv exists
        if os.path.exists(self.csv_path):
            console.print(f"[green]✔ Dataset found at {self.csv_path}.[/green]")
            return

        # 2. Check if tweets.zip exists, if not download
        if not os.path.exists(self.zip_path):
            console.print("[yellow]Dataset missing. Downloading tweets.zip...[/yellow]")
            try:
                with requests.get(self.repo_url, stream=True) as r:
                    r.raise_for_status()
                    total_size = int(r.headers.get('content-length', 0))
                    
                    with open(self.zip_path, 'wb') as f, Progress(
                        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TaskProgressColumn()
                    ) as progress:
                        task = progress.add_task("[cyan]Downloading...", total=total_size)
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))
                            
                console.print(f"[green]✔ Download complete: {self.zip_path}[/green]")
            except Exception as e:
                console.print(f"[red] Download failed: {e}[/red]")
                return

        # 3. Validating Zip
        if not os.path.exists(self.zip_path): 
             console.print(f"[red] Error: {self.zip_path} not found after download attempt.[/red]")
             return

        # 4. Extracting and Renaming
        console.print("[yellow]Extracting tweets.csv from zip...[/yellow]")
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                # The file inside the repo structure
                # We know the structure: turkish-tweets-sentiment-analysis-master/data/TurkishTweets.csv
                # But let's search for it to be safe
                target_file = None
                for file_name in zip_ref.namelist():
                    if file_name.endswith("TurkishTweets.csv"):
                        target_file = file_name
                        break
                
                if target_file:
                    with zip_ref.open(target_file) as source, open(self.csv_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                    console.print(f"[green]✔ Extracted and renamed to {self.csv_path}.[/green]")
                else:
                    console.print("[red] 'TurkishTweets.csv' not found within the zip.[/red]")
        except zipfile.BadZipFile:
            console.print("[red] Error: The downloaded file is not a valid zip.[/red]")

    def _get_fallback_mock_data(self, count):
        """Fallback mock data if CSV is missing."""
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
        
        data = []
        for _ in range(count):
            data.append({
                "id": str(uuid.uuid4()),
                "text": random.choice(mock_templates),
                "user": random.choice(self.users),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "platform": "Twitter (Mock)"
            })
        return data

    def generate_data(self, count=50):
        self._download_and_extract_if_needed()
        
        print(f"Loading real tweets from local dataset...")
        
        if os.path.exists(self.csv_path):
            try:
                df = pd.read_csv(self.csv_path)
                # Drop rows with NaN in 'Tweet' column
                df = df.dropna(subset=['Tweet'])
                
                # Sample random rows
                if len(df) > count:
                    sample = df.sample(n=count)
                else:
                    sample = df
                
                data = []
                for _, row in sample.iterrows():
                    # The dataset has 'Tweet' column
                    text = str(row['Tweet']) # Ensure string
                    
                    # Randomize date within last 30 days
                    days_back = random.randint(0, 30)
                    date = datetime.now() - timedelta(days=days_back, minutes=random.randint(0, 1440))
                    
                    record = {
                        "id": str(uuid.uuid4()),
                        "text": text,
                        "user": random.choice(self.users),
                        "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                        "platform": "Twitter (Dataset)"
                    }
                    data.append(record)
                
                print(f"Successfully loaded {len(data)} tweets from dataset.")
                return pd.DataFrame(data)
                
            except Exception as e:
                print(f"Error reading CSV: {e}")
        
        print("CSV not found or error. Using mock data.")
        return pd.DataFrame(self._get_fallback_mock_data(count))

if __name__ == "__main__":
    dc = DataCollector()
    df = dc.generate_data(5)
    print(df)
