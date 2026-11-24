# ✦ Aura: Kişisel AI Asistan & Model Karşılaştırma

OpenRouter üzerinden çalışan, yerelde (localhost) koşan kişisel bir chatbot ve farklı LLM'leri hız, maliyet ve kalite açısından karşılaştıran bir evaluation aracı.

## Özellikler

- 💬 **Sohbet arayüzü:** pembe-gold temalı, Markdown destekli, sohbet geçmişini tarayıcıda saklayan web arayüzü
- 🧠 **Kişiselleştirilebilir persona:** botun kişiliği ve kuralları `persona.txt` dosyasından okunur (system prompt)
- 🔒 **Güvenlik:** API anahtarı `.env`'de tutulur, model çıktıları DOMPurify ile temizlenerek gösterilir
- 📊 **Model evaluation:** aynı soruları birden fazla modele sorup süre, token ve maliyeti CSV olarak kaydeder

## Kullanılan Teknolojiler

- **Backend:** Python, Flask, Requests
- **Frontend:** HTML, CSS, JavaScript, marked.js, DOMPurify
- **LLM API:** OpenRouter

## Kurulum

```bash
git clone https://github.com/Eminenurdogan/chatbot-evaluation-project.git
cd chatbot-evaluation-project
python -m venv venv
venv\Scripts\activate        # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

Ardından:

1. `.env.example` dosyasını kopyalayıp adını `.env` yap, kendi [OpenRouter API anahtarını](https://openrouter.ai/keys) yaz.
2. (İsteğe bağlı) Ana klasöre `persona.txt` adında bir dosya oluşturup botun kişiliğini yaz. Dosya yoksa varsayılan bir asistan olarak çalışır.

## Kullanım

**Chatbot:**

```bash
python app.py
```

Tarayıcıda `http://127.0.0.1:5000` adresini aç.

**Model karşılaştırma:**

```bash
python evaluate.py     # soruları modellere sorar, results/ klasörüne CSV kaydeder
python summarize.py    # son sonuç dosyasının özet tablosunu yazdırır
```

## Evaluation Sonuçları

5 soru (yapay zekâ, siber güvenlik, Python, kariyer) × 3 model, aynı persona ile test edildi:

| Model               | Ort. süre | Ort. çıktı token | Toplam maliyet |
| ------------------- | --------- | ---------------- | -------------- |
| DeepSeek V4.1 Flash | 5.8 sn    | 1051             | $0.0037        |
| Claude Haiku 5.5    | 7.1 sn    | 1218             | $0.0035        |
| Qwen3.8 Flash       | 15.9 sn   | 1165             | $0.0032        |

**Kalite değerlendirmesi:**

- **Claude Haiku 5.5:** persona kurallarına en tutarlı uyan, Türkçe hatası olmayan model. **Aura için seçildi.**
- **DeepSeek V4.1 Flash:** en hızlı ve teknik açıdan en detaylı, ama persona ve Türkçe tutarlılığı daha zayıf.
- **Qwen3.8 Flash:** reasoning modeli olduğu için en yavaşı, bazı cevapları gereğinden uzun.

## Proje Yapısı

```
├── app.py                # Flask sunucusu ve OpenRouter bağlantısı
├── evaluate.py           # Model karşılaştırma script'i
├── summarize.py          # Sonuç özeti
├── templates/index.html  # Sohbet arayüzü
├── static/logo.svg       # Logo
├── persona.example.txt   # Örnek persona (system prompt)
├── .env.example          # Örnek ortam değişkenleri
└── requirements.txt
```
