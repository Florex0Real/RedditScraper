# 🔍 Reddit Scraper

Reddit verilerini çekip analiz etmek için kullanıcı dostu bir Streamlit uygulaması. Ücretsiz Reddit API erişimi ile subreddit gönderilerini çekebilir, filtreleyebilir ve CSV formatında dışa aktarabilirsiniz.

## ✨ Özellikler

### 🎭 Demo Modu
- API anahtarı olmadan örnek verilerle test edebilirsiniz
- Arayüzü keşfetmek için hemen başlayın

### 🔑 Kişisel API Erişimi
- Kendi ücretsiz Reddit API kimlik bilgilerinizi kolayca girebilirsiniz
- Gerçek Reddit verilerine güvenli erişim
- Adım adım kurulum rehberi dahil

### 📊 Veri Çekme Özellikleri
- **Çoklu gönderi türleri**: Hot, new, top gönderiler
- **Zaman filtreleri**: Günlük, haftalık, aylık, yıllık veya tüm zamanlar
- **Akıllı filtreleme**: Puan ve yorum sayısına göre filtreleme
- **Gerçek zamanlı ilerleme**: Çekme işlemi sırasında durum güncellemeleri

### 💾 Dışa Aktarma
- CSV formatında veri indirme
- Otomatik dosya adlandırma
- Filtrelenmiş verileri kaydetme

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
git clone https://github.com/yourusername/reddit-scraper.git
cd reddit-scraper
pip install -r requirements.txt
```

### 2. Uygulamayı Çalıştırma

```bash
streamlit run app.py
```

### 3. Tarayıcıda Açma

Uygulama otomatik olarak `http://localhost:8501` adresinde açılacaktır.

## 🔧 Reddit API Kurulumu (Ücretsiz)

### Adım 1: Reddit Hesabı
Reddit hesabınızla [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) adresine gidin.

### Adım 2: Uygulama Oluşturma
1. **"Create App"** veya **"Create Another App"** butonuna tıklayın
2. Formu doldurun:
   - **Name**: Uygulamanızın adı (ör: "Benim Reddit Scraper'ım")
   - **App type**: **"script"** seçeneğini seçin
   - **Description**: İsteğe bağlı
   - **About URL**: Boş bırakın
   - **Redirect URI**: `http://localhost:8080`
3. **"Create app"** butonuna tıklayın

### Adım 3: Kimlik Bilgilerini Alma
- **Client ID**: Uygulama adının altında görünen kısa string
- **Client Secret**: "reveal" butonuna tıklayarak görebileceğiniz uzun string

### Adım 4: Uygulamada Kullanma
Streamlit arayüzünde bu bilgileri girin ve "Connect to Reddit API" butonuna tıklayın.

## 📋 Kullanım

### Demo Modu
1. **"Try Demo Mode"** butonuna tıklayın
2. Örnek verilerle arayüzü keşfedin
3. Tüm özelliklerini test edin

### Gerçek Veri Çekme
1. Reddit API kimlik bilgilerinizi girin
2. Çekmek istediğiniz subreddit adını yazın (r/ olmadan)
3. Gönderi türünü seçin (hot, new, top)
4. Çekilecek gönderi sayısını ayarlayın
5. **"Scrape Posts"** butonuna tıklayın

### Filtreleme ve Dışa Aktarma
1. Minimum puan ve yorum sayısı filtrelerini ayarlayın
2. Sonuçları inceleyin
3. **"Export to CSV"** ile verileri indirin

## 📁 Proje Yapısı

```
reddit-scraper/
├── app.py                 # Ana Streamlit uygulaması
├── reddit_scraper.py      # Reddit API işlevleri
├── requirements.txt       # Python bağımlılıkları
├── .streamlit/
│   └── config.toml       # Streamlit yapılandırması
└── README.md             # Bu dosya
```

## 🛠️ Teknolojiler

- **[Streamlit](https://streamlit.io/)**: Web arayüzü framework'ü
- **[PRAW](https://praw.readthedocs.io/)**: Python Reddit API Wrapper
- **[Pandas](https://pandas.pydata.org/)**: Veri işleme ve analiz
- **[Python 3.11+](https://python.org/)**: Programlama dili

## 📊 Çekilen Veriler

Her gönderi için şu bilgiler çekilir:
- Başlık ve URL
- Yazar bilgileri
- Puan ve upvote oranı
- Yorum sayısı
- Oluşturulma tarihi ve saati
- Gönderi içeriği (metin gönderileri için)
- Gönderi türü (metin/link)
- Domain bilgisi
- Özel etiketler (over_18, spoiler, stickied, locked)

## ⚖️ Yasal ve Etik Kullanım

- Reddit'in resmi API'sini kullanır
- Rate limiting kurallarına uyar
- Kullanım şartlarını respects eder
- Kişisel ve araştırma amaçlı kullanım için tasarlanmıştır

## 🤝 Katkıda Bulunma

1. Bu repo'yu fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 🆘 Destek

Herhangi bir sorunla karşılaşırsanız:
1. [Issues](https://github.com/yourusername/reddit-scraper/issues) sayfasında arayın
2. Yeni issue açın
3. Demo modu ile test edip sonucu paylaşın

## 🔄 Güncellemeler

### v1.0.0
- ✅ İlk sürüm yayınlandı
- ✅ Demo modu eklendi
- ✅ Kullanıcı dostu API kurulumu
- ✅ CSV dışa aktarma özelliği
- ✅ Akıllı filtreleme sistemi

---

**Not**: Bu uygulama sadece public subredditlerden veri çekebilir. Private veya restricted subredditlere erişim sağlamaz.