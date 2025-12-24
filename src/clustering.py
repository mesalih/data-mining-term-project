from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

class TopicClusterer:
    def __init__(self, n_clusters=3):
        self.n_clusters = n_clusters
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')

    def cluster(self, texts):
        """
        Applies TF-IDF vectorization and K-Means clustering.
        Returns the cluster labels and the transformed matrix.
        """
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        self.model.fit(tfidf_matrix)
        
        return self.model.labels_

    def get_cluster_keywords(self, n_terms=5):
        """
        Returns the top keywords for each cluster centroind.
        """
        if not hasattr(self.model, 'cluster_centers_'):
            return {}

        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        terms = self.vectorizer.get_feature_names_out()
        
        cluster_keywords = {}
        for i in range(self.n_clusters):
            top_terms = [terms[ind] for ind in order_centroids[i, :n_terms]]
            cluster_keywords[i] = top_terms
            
        return cluster_keywords

if __name__ == "__main__":
    sample_texts = [
        "Yapay zeka çok hızlı gelişiyor",
        "AI is evolving fast",
        "Spor yapmak sağlıklıdır",
        "Futbol maçı çok heyecanlıydı",
        "Ekonomi kötüye gidiyor",
        "Dolar kuru yükseldi"
    ]
    clusterer = TopicClusterer(n_clusters=3)
    labels = clusterer.cluster(sample_texts)
    print("Labels:", labels)
    print("Keywords:", clusterer.get_cluster_keywords())
