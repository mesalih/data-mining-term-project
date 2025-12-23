# Social Media Data Mining Project

Bu proje, Sosyal Medya verileri üzerinde Veri Madenciliği tekniklerini (Ön işleme, Duygu Analizi, Kümeleme) uygulamalı olarak göstermektedir. Proje, Python dili ve `rich` kütüphanesi kullanılarak interaktif bir terminal uygulaması olarak tasarlanmıştır.

## Özellikler

- **Veri Toplama**: Google Gemini API kullanılarak gerçekçi tweet verisi üretimi (veya API anahtarı yoksa yedek mock veri).
- **Ön İşleme**: Temizleme, normalizasyon ve kök bulma işlemleri.
- **Duygu Analizi**: Naive Bayes algoritması ile metinlerin pozitif/negatif/nötr olarak sınıflandırılması.
- **Kümeleme**: K-Means algoritması ile metinlerin konu başlıklarına göre gruplandırılması.

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
