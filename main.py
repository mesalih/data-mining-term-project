import time
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from src.data_collector import DataCollector
from src.preprocessor import Preprocessor
from src.sentiment_analyzer import SentimentAnalyzer
from src.clustering import TopicClusterer

console = Console()

def main():
    console.clear()
    console.print(Panel.fit("[bold cyan]Social Media Data Mining Project[/bold cyan]\n[yellow]Analysis of Trends & Sentiments[/yellow]", border_style="blue"))
    time.sleep(1)

    # 1. Data Collection
    console.print("\n[bold green]1. Data Collection Phase[/bold green]")
    collector = DataCollector(topic="Yapay Zeka")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Connecting to (Mock) Social Media API...", total=10)
        time.sleep(1)
        progress.update(task, description="Fetching Tweets...", advance=5)
        time.sleep(1)
        df = collector.generate_data(count=100) # Generating 100 rows
        progress.update(task, completed=10)

    console.print(f"✅ Successfully collected [bold]{len(df)}[/bold] items.")
    
    # Show Raw Data Sample
    table = Table(title="Raw Data Sample (First 5)")
    table.add_column("Date", style="dim", width=12)
    table.add_column("User", style="magenta")
    table.add_column("Content", style="white")
    
    for _, row in df.head(5).iterrows():
        table.add_row(str(row['date'])[:10], row['user'], row['text'][:50] + "...")
    console.print(table)
    time.sleep(1)

    # 2. Preprocessing
    console.print("\n[bold green]2. Preprocessing Phase[/bold green]")
    preprocessor = Preprocessor()
    
    processed_texts = []
    with Progress() as progress:
        task = progress.add_task("[cyan]Cleaning, Normalizing, Stemming...", total=len(df))
        for text in df['text']:
            processed = preprocessor.process(text)
            processed_texts.append(processed)
            progress.update(task, advance=1)
            time.sleep(0.01) # Simulate work
    
    df['processed_text'] = processed_texts
    console.print("✅ Preprocessing complete.")
    console.print(f"[italic]Example transformation:[/italic]\n[red]Original:[/red] {df['text'].iloc[0]}\n[green]Processed:[/green] {df['processed_text'].iloc[0]}")
    time.sleep(1)

    # 3. Sentiment Analysis
    console.print("\n[bold green]3. Sentiment Analysis Phase (Classification)[/bold green]")
    analyzer = SentimentAnalyzer()
    
    with console.status("[bold green]Training Naive Bayes Model on historical data...[/bold green]"):
        analyzer.train_mock_model()
        time.sleep(1.5)
    
    sentiments = analyzer.predict_batch(df['processed_text'])
    df['sentiment'] = sentiments
    
    # Stats
    sentiment_counts = df['sentiment'].value_counts()
    console.print(Panel(f"Positive: {sentiment_counts.get('Positive', 0)}\nNegative: {sentiment_counts.get('Negative', 0)}\nNeutral: {sentiment_counts.get('Neutral', 0)}", title="Sentiment Distribution", border_style="green"))

    # 4. Clustering
    console.print("\n[bold green]4. Topic Clustering Phase (Unsupervised)[/bold green]")
    clusterer = TopicClusterer(n_clusters=3)
    
    with console.status("[bold blue]Running K-Means Clustering...[/bold blue]"):
        labels = clusterer.cluster(df['processed_text'])
        time.sleep(1)
    
    df['cluster'] = labels
    keywords = clusterer.get_cluster_keywords()
    
    cluster_table = Table(title="Discovered Topics & Clusters")
    cluster_table.add_column("Cluster ID", justify="center")
    cluster_table.add_column("Top Keywords", style="cyan")
    cluster_table.add_column("Count", justify="right")
    
    for cluster_id in range(3):
        count = len(df[df['cluster'] == cluster_id])
        keys = ", ".join(keywords.get(cluster_id, []))
        cluster_table.add_row(str(cluster_id), keys, str(count))
        
    console.print(cluster_table)

    # Final Output
    console.print("\n[bold yellow]Analysis Complete! Saving results...[/bold yellow]")
    df.to_csv("results_output.csv", index=False)
    console.print("Saved to [bold]results_output.csv[/bold]")

    # Visualization Prompt (Streamlit)
    from rich.prompt import Confirm
    import subprocess
    import sys
    
    if Confirm.ask("\n[bold cyan]Do you want to visualize the results (Streamlit Dashboard)?[/bold cyan]"):
        console.print("[green]Launching Streamlit App...[/green]")
        console.print("[dim]Press Ctrl+C to stop the dashboard server.[/dim]")
        try:
            # Run "streamlit run src/dashboard_app.py"
            subprocess.run([sys.executable, "-m", "streamlit", "run", "src/dashboard_app.py"], check=True)
        except KeyboardInterrupt:
            console.print("\n[yellow]Dashboard stopped.[/yellow]")
        except Exception as e:
            console.print(f"[bold red]Error launching dashboard:[/bold red] {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Process interrupted by user.[/bold red]")
