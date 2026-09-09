# OVO Checker Bot 🤖

Bot Telegram untuk mengecek apakah nomor HP terdaftar di OVO atau belum.

## Fitur ✨

- ✅ Cek status registrasi nomor OVO
- ✅ Validasi format nomor HP
- ✅ Response cepat dengan caching
- ✅ Fallback heuristic jika API tidak tersedia
- ✅ User-friendly interface
- ✅ Async support untuk performa maksimal

## Persyaratan 📋

- Python 3.8 atau lebih tinggi
- pip atau conda
- Telegram Bot Token (dari @BotFather)

## Instalasi 🚀

### 1. Clone Repository
```bash
git clone https://github.com/Riski1610/ovo-checker-bot.git
cd ovo-checker-bot
```

### 2. Buat Virtual Environment (Optional tapi Recommended)
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\\Scripts\\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
cp .env.example .env
```

Edit file `.env` dan masukkan Telegram Bot Token Anda:
```env
TELEGRAM_TOKEN=your_token_here
```

### 5. Jalankan Bot
```bash
python src/main.py
```

## Penggunaan 📱

### Commands
- `/start` - Tampilkan menu utama
- `/help` - Bantuan penggunaan
- `/about` - Tentang bot

### Cara Mengecek Nomor
1. Kirim nomor HP ke bot
2. Format yang diterima:
   - `08xxxxxxxxxx`
   - `+628xxxxxxxxxx`
   - `628xxxxxxxxxx`

### Contoh Response
```
✅ Hasil Pengecekan

📱 Nomor: 081234567890
📊 Status: TERDAFTAR
⏰ Waktu: 09/09/2026, 17:59:23
```

## Struktur Project 📁

```
ovo-checker-bot/
├── src/
│   ├── main.py                 # Main bot file
│   └── services/
│       ├── __init__.py
│       └── ovo_checker.py      # OVO checker logic
├── requirements.txt             # Dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
└── README.md                    # Dokumentasi
```

## Cara Kerja 🔧

### Flow Pengecekan

```
User Input Nomor
    ↓
Validasi Format
    ↓
Cek Cache
    ├→ Ada → Return Cached Result
    └→ Tidak Ada ↓
    ↓
Try OVO API
    ├→ Success → Cache & Return
    └→ Failed ↓
    ↓
Fallback Heuristic
    ↓
Cache Result
    ↓
Return to User
```

### Methods

1. **OVO API (Primary)**
   - Menghubungi endpoint OVO resmi (jika tersedia)
   - Paling akurat

2. **Heuristic (Fallback)**
   - Pattern matching berdasarkan nomor
   - Bisa dioptimalkan dengan data real

3. **Caching**
   - Cache result selama 1 jam
   - Mengurangi API calls

## Konfigurasi 🛠️

### Timeout API
Default timeout API call: **10 detik**

Edit di `src/services/ovo_checker.py`:
```python
timeout=aiohttp.ClientTimeout(total=10)
```

### Cache Expiry
Default cache expiry: **1 jam (3600 detik)**

Edit di `src/services/ovo_checker.py`:
```python
self.cache_expiry = 3600  # seconds
```

## Development Tips 💡

### Testing Bot Lokal
```bash
python src/main.py
```

### Debug Mode
Edit logging level di `src/main.py`:
```python
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Change from INFO to DEBUG
)
```

### Database Integration
Untuk hasil yang lebih akurat, integrasikan dengan database nomor terdaftar OVO:

```python
# Contoh di ovo_checker.py
async def _check_via_database(self, phone_number: str) -> dict:
    # Query database untuk cek nomor
    # return hasil dari database
    pass
```

## Troubleshooting 🐛

### Bot Tidak Merespons
1. Cek token di `.env`
2. Restart bot
3. Cek internet connection
4. Cek bahwa Telegram token valid di @BotFather

### API Error
1. Check log messages untuk error details
2. OVO API mungkin sedang down
3. Bot akan fallback ke heuristic

## Security ⚠️

- ⚠️ Jangan share `.env` file Anda
- ⚠️ Simpan token di environment variable
- ⚠️ Validasi semua input user
- ⚠️ Jangan commit `.env` ke repository

## Disclaimer ⚡

Bot ini dibuat untuk keperluan edukasi dan verifikasi nomor OVO. Gunakan sesuai dengan ToS OVO dan peraturan yang berlaku.

## Requirements 📦

```
python-telegram-bot==20.3
requests==2.31.0
python-dotenv==1.0.0
aiohttp==3.9.0
```

## License 📄

MIT License - Feel free to use this project

## Support & Kontribusi 🤝

Punya pertanyaan atau saran? Buat issue atau pull request!

---

Made with ❤️ by Riski1610
