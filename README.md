# Pegasus Info 🦅

Pegasus Info adalah sistem intelijen informasi yang bertugas mengambil, mengolah, dan menganalisis berita online gratis dari berbagai media terbuka.

## 📋 Fitur Utama

### 📰 News Scraper (Gratis)
- Ambil berita dari RSS feed publik
- Mendukung berbagai media nasional & internasional
- Tanpa API berbayar

### 🏥 Modul Kesehatan
- Deteksi wabah & penyakit
- Informasi obat & vaksin
- Kebijakan kesehatan
- Kata kunci: WHO, outbreak, virus, vaccine, hospital

### 🪖 Modul Militer & Keamanan
- Deteksi konflik bersenjata
- Latihan militer
- Senjata & alutsista
- Kata kunci: missile, army, drone, navy, defense

### 💰 Modul Uang & Ekonomi
- Deteksi inflasi
- Bank & suku bunga
- Kripto & saham
- Kata kunci: inflation, bitcoin, bank, dollar, market

### 📈 Deteksi Berita Booming
- Berdasarkan jumlah kemunculan topik
- Analisis banyaknya media membahas topik sama
- Update cepat dalam waktu singkat

### 🧠 Analisis Konteks
- Analisis dampak (High/Medium/Low)
- Sentimen berita (Positif/Negatif/Netral)
- Ekstraksi entitas (lokasi, organisasi, negara)

### ✍️ Auto Ringkasan
- Ringkasan 1-2 paragraf
- Bahasa netral & informatif
- Tanpa opini

### 🗂 Klasifikasi Otomatis
- Kesehatan
- Militer
- Uang & Ekonomi
- Campuran (jika overlap)

### 🔔 Alert Topik Sensitif
- Peringatan otomatis untuk:
  - Wabah baru
  - Konflik meningkat
  - Krisis finansial

### 📤 Export & Arsip
- JSON
- CSV
- Markdown report

## 🚀 Instalasi

### Prerequisites
- Python 3.7 atau lebih tinggi
- pip (Python package manager)

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 📖 Penggunaan

### Jalankan Pipeline Lengkap
```bash
python pegasus_info.py
```

### Opsi Tambahan
```bash
# Ambil berita dari 12 jam terakhir
python pegasus_info.py --hours 12

# Ambil berita tanpa export
python pegasus_info.py --no-export

# Filter berdasarkan kategori
python pegasus_info.py --category health
```

### Penggunaan di Python
```python
from pegasus_info import PegasusInfo

# Inisialisasi
pegasus = PegasusInfo()

# Jalankan pipeline lengkap
results = pegasus.run_full_pipeline(hours=24, export=True)

# Akses artikel
articles = results['articles']

# Akses trending topics
trending = results['trending']

# Akses analysis
analysis = results['analysis']
```

### Fetch & Classify Saja
```python
# Ambil dan klasifikasikan artikel
classified = pegasus.fetch_and_classify(hours=24)

# Cek hasil
for article in classified:
    print(f"Title: {article['title']}")
    print(f"Category: {article['primary_category']}")
    print(f"Impact: {article['impact_level']}")
    print(f"Sentiment: {article['sentiment']}")
    print(f"Sensitive: {article['is_sensitive']}")
    print("-" * 60)
```

### Dapatkan Trending Topics
```python
# Dapatkan trending topics
trending = pegasus.get_trending(hours=24)

# Cek top keywords
for keyword, count in trending['trending_keywords']:
    print(f"{keyword}: {count} mentions")
```

## 📂 Struktur Project

```
pegasus-info/
├── pegasus_info.py       # Main application
├── scraper.py           # News scraper module
├── classifier.py        # News classifier module
├── trending.py          # Trending detection module
├── analyzer.py          # Analysis module
├── summarizer.py        # Summary generation module
├── exporter.py          # Export module
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
└── exports/             # Exported reports (auto-created)
```

## ⚙️ Konfigurasi

Edit `config.py` untuk mengubah:

- RSS Feed Sources
- Keywords untuk setiap kategori
- Sensitive topic alerts
- Trending detection thresholds
- Export settings

## 📊 Output

### Article Fields
Setiap artikel memiliki field:

- `title` - Judul berita
- `link` - URL berita
- `summary` - Ringkasan berita
- `published_date` - Tanggal publikasi
- `category` - Kategori asal
- `source` - Sumber media
- `primary_category` - Kategori utama (setelah klasifikasi)
- `secondary_categories` - Kategori tambahan
- `impact_level` - Level dampak (high/medium/low)
- `sentiment` - Sentimen (positive/negative/neutral)
- `is_sensitive` - Apakah topik sensitif
- `sensitive_topics` - Daftar topik sensitif
- `entities` - Entitas yang terdeteksi
- `insight` - Insight singkat

### Export Formats
Semua format disimpan di folder `exports/`:

- `news_TIMESTAMP.json` - Format JSON lengkap
- `news_TIMESTAMP.csv` - Format CSV
- `news_TIMESTAMP.md` - Format Markdown report
- `trending_TIMESTAMP.md` - Report trending topics

## 🔍 Contoh Output

### JSON Format
```json
{
  "metadata": {
    "exported_at": "2024-01-15T10:30:00",
    "total_articles": 50,
    "format": "json"
  },
  "articles": [
    {
      "title": "WHO announces new vaccine rollout",
      "link": "https://example.com/article",
      "summary": "World Health Organization...",
      "primary_category": "health",
      "impact_level": "high",
      "sentiment": "positive",
      "is_sensitive": true,
      "insight": "⚠️ SENSITIVE: This health news requires attention..."
    }
  ]
}
```

### Markdown Format
```markdown
# Pegasus Info News Report

**Generated:** 2024-01-15 10:30:00
**Total Articles:** 50

---

## Health
**Articles:** 15

---

### 1. WHO announces new vaccine rollout
**Source:** who.int
**Date:** 2024-01-15T08:00:00
**Category:** Health
**Impact:** 🔴 High
**Status:** ⚠️ SENSITIVE

**Summary:**
World Health Organization announces new vaccine rollout...

**Insight:**
⚠️ SENSITIVE: This health news requires attention...
```

## 📝 Catatan

- Sistem menggunakan RSS feed publik (gratis)
- Rate limiting diimplementasikan untuk menghindari pemblokiran
- Artikel duplikat otomatis dihapus
- Semua proses menggunakan logger untuk tracking

## 🤝 Kontribusi

Sistem ini open-source dan dapat dikembangkan lebih lanjut.

## 👤 Author & Kontak

- **Author:** Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE
- **GitHub:** https://github.com/sobri3195
- **Email:** muhammadsobrimaulana31@gmail.com

## 🌐 Link & Sosial Media

- YouTube: https://www.youtube.com/@muhammadsobrimaulana6013
- Telegram: https://t.me/winlin_exploit
- TikTok: https://www.tiktok.com/@dr.sobri
- Grup WhatsApp: https://chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl
- Website: https://muhammadsobrimaulana.netlify.app
- Toko Online Sobri: https://pegasus-shop.netlify.app
- Gumroad: https://maulanasobri.gumroad.com/
- Sevalla Page: https://muhammad-sobri-maulana-kvr6a.sevalla.page/

## 💖 Donasi

- https://lynk.id/muhsobrimaulana
- https://trakteer.id/g9mkave5gauns962u07t
- https://karyakarsa.com/muhammadsobrimaulana
- https://nyawer.co/MuhammadSobriMaulana

## 📄 Lisensi

Free untuk penggunaan edukasi dan riset.

## 🔐 Privasi

- Tidak menggunakan API berbayar
- Tidak menyimpan data pribadi
- Data hanya dari sumber publik

## 👨‍💻 Author

**Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE**

- 📧 **Email:** muhammadsobrimaulana31@gmail.com
- 🐙 **GitHub:** [@sobri3195](https://github.com/sobri3195)

### 🔗 Links & Media

#### Donation & Support
- **Lynk.id:** [lynk.id/muhsobrimaulana](https://lynk.id/muhsobrimaulana)
- **Trakteer:** [trakteer.id/g9mkave5gauns962u07t](https://trakteer.id/g9mkave5gauns962u07t)
- **Gumroad:** [maulanasobri.gumroad.com](https://maulanasobri.gumroad.com/)
- **KaryaKarsa:** [karyakarsa.com/muhammadsobrimaulana](https://karyakarsa.com/muhammadsobrimaulana)
- **Nyawer:** [nyawer.co/MuhammadSobriMaulana](https://nyawer.co/MuhammadSobriMaulana)

#### Social Media & Contact
- **YouTube:** [@muhammadsobrimaulana6013](https://www.youtube.com/@muhammadsobrimaulana6013)
- **Telegram:** [@winlin_exploit](https://t.me/winlin_exploit)
- **TikTok:** [@dr.sobri](https://www.tiktok.com/@dr.sobri)
- **WhatsApp Group:** [Join Group](https://chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl)

#### Websites & Services
- **Personal Website:** [muhammadsobrimaulana.netlify.app](https://muhammadsobrimaulana.netlify.app)
- **Portfolio:** [muhammad-sobri-maulana-kvr6a.sevalla.page](https://muhammad-sobri-maulana-kvr6a.sevalla.page/)
- **Toko Online:** [pegasus-shop.netlify.app](https://pegasus-shop.netlify.app)

---

**Pegasus Info** - News Intelligence System
🦅 Intelijen Berita untuk Masa Depan
