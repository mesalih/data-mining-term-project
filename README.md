# Social Media Data Mining Project

Bu proje, Sosyal Medya verileri üzerinde Veri Madenciliği tekniklerini (Ön işleme, Duygu Analizi, Kümeleme) uygulamalı olarak göstermektedir. Proje, Python dili ve `rich` kütüphanesi kullanılarak interaktif bir terminal uygulaması olarak tasarlanmıştır.

## 🚀 Özellikler (Features)

1.  **Veri Toplama (Data Collection)**:

    - **Google Gemini API (google-genai)** kullanılarak gerçekçi, tekrar etmeyen tweet verileri üretilir.
    - API anahtarı yoksa otomatik olarak "Mock" (sahte) veriye geçiş yapar.
    - Veriler `date`, `user`, `text`, `platform` alanlarını içerir.

2.  **Ön İşleme (Preprocessing)**:

    - Temizleme: URL'ler, mention'lar (@user), hashtag'ler ve özel karakterler temizlenir.
    - Normalizasyon: Metin küçük harfe çevrilir.
    - Kök Bulma (Stemming): Kelimeler köklerine indirgenir.
    - Stopwords: Gereksiz kelimeler çıkarılır.

3.  **Duygu Analizi (Sentiment Analysis)**:

    - Naïve Bayes sınıflandırıcısı ile metinler **Pozitif**, **Negatif** veya **Nötr** olarak etiketlenir.

4.  **Konu Kümeleme (Topic Clustering)**:

    - K-Means algoritması ile tweetler benzerliklerine göre gruplanır.
    - Her küme için anahtar kelimeler (keywords) çıkarılır.

5.  **Görselleştirme & Sunum (Visualization)**:
    - **CLI (Terminal)**: `rich` kütüphanesi ile renkli, dinamik akış.
    - **Dashboard (Web)**: `streamlit` ile geliştirilmiş "Next-Level" interaktif panel.
      - Filtreleme (Duygu/Konu), Arama, İnteraktif Grafikler (Plotly).

## Kurulum ve Çalıştırma

Lütfen aşağıdaki adımları sırasıyla terminalinizde uygulayınız.

### 1. Gereksinimler

- Python 3.9 veya üzeri
- [Opsiyonel] Google Gemini API Anahtarı (Daha gerçekçi veri üretimi için)

### 2. Proje Dosyalarına Gitme

Terminali açın ve proje klasörüne gidin:

```bash
cd "/path/to/project_folder"
```

### 3. Sanal Ortam Oluşturma (Virtual Environment)

Sistem kütüphanelerini etkilememek için sanal ortam oluşturun:

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Kütüphanelerin Yüklenmesi

Gerekli paketleri `requirements.txt` dosyasından yükleyin:

```bash
pip install -r requirements.txt
```

### 5. Uygulamayı Çalıştırma

Her şey hazır! Uygulamayı başlatmak için:

```bash
python main.py
```

Program analizleri tamamladıktan sonra size **Dashboard'u açmak isteyip istemediğinizi** soracaktır:

> **Do you want to visualize the results (Streamlit Dashboard)? [y/n]**

`y` yazıp onaylarsanız, tarayıcınızda açılan **Streamlit Dashboard** üzerinden verileri interaktif olarak inceleyebilirsiniz.

## API Anahtarı Hakkında (Opsiyonel)

Proje varsayılan olarak **API anahtarı olmadan da çalışır**. Bu durumda önceden hazırlanmış şablon verileri kullanır.

Eğer gerçek zamanlı yapay zeka tarafından üretilen verilerle denemek isterseniz:

1.  Proje ana dizininde `.env` adında bir dosya oluşturun.
2.  İçerisine şu satırı ekleyin:
    ```
    GEMINI_API_KEY=AIzaSy... (Sizin anahtarınız)
    ```
3.  Uygulamayı yeniden başlatın.

## Çıktılar

Program çalıştıktan sonra sonuçları ekranda dinamik olarak gösterir ve analiz edilen veriyi `results_output.csv` dosyasına kaydeder.
