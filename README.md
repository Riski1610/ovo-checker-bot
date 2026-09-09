# OVO Checker Bot 🤖

Bot Telegram untuk mengecek apakah nomor HP terdaftar di OVO atau belum.

## Fitur ✨

- ✅ Cek status registrasi nomor OVO
- ✅ Validasi format nomor HP
- ✅ Response cepat dengan caching
- ✅ Fallback heuristic jika API tidak tersedia
- ✅ User-friendly interface

## Persyaratan 📋

- Node.js v14 atau lebih tinggi
- npm atau yarn
- Telegram Bot Token (dari @BotFather)

## Instalasi 🚀

### 1. Clone Repository
```bash
git clone https://github.com/Riski1610/ovo-checker-bot.git
cd ovo-checker-bot
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Setup Environment Variables
```bash
cp .env.example .env
```

Edit file `.env` dan masukkan Telegram Bot Token Anda:
```env
TELEGRAM_TOKEN=your_token_here
```

### 4. Jalankan Bot
```bash
# Production
npm start

# Development (dengan auto-reload)
npm run dev
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
⏰ Waktu: 9/9/2026, 17:59:23
```

## Struktur Project 📁

```
ovo-checker-bot/
├── src/
│   ├── index.js              # Main bot file
│   └── services/
│       └── ovoChecker.js     # OVO checker logic
├── package.json              # Dependencies
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
└── README.md                 # Dokumentasi
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

### Timeout
Default timeout API call: **10 detik**

Edit di `src/services/ovoChecker.js`:
```javascript
timeout: 10000 // milliseconds
```

### Cache Expiry
Default cache expiry: **1 jam (3600000 ms)**

Edit di `src/services/ovoChecker.js`:
```javascript
this.cacheExpiry = 3600000;
```

## Development Tips 💡

### Testing Bot Lokal
```bash
npm run dev
```

### Debug Mode
Uncomment logging di `src/services/ovoChecker.js`

### Database Integration
Untuk hasil yang lebih akurat, integrasikan dengan database nomor terdaftar OVO:

```javascript
// Contoh di ovoChecker.js
async checkViaDatabase(phoneNumber) {
  const result = await db.query('SELECT * FROM ovo_users WHERE phone = ?', [phoneNumber]);
  return result.length > 0;
}
```

## Troubleshooting 🐛

### Bot Tidak Merespons
1. Cek token di `.env`
2. Restart bot
3. Cek internet connection

### API Error
1. Check log messages
2. OVO API mungkin sedang down
3. Bot akan fallback ke heuristic

### Cache Issue
Clear cache manual:
```javascript
// Di terminal Node.js
const ovoChecker = require('./src/services/ovoChecker');
ovoChecker.clearCache();
```

## Security ⚠️

- ⚠️ Jangan share `.env` file Anda
- ⚠️ Simpan token di environment variable
- ⚠️ Validasi semua input user

## Disclaimer ⚡

Bot ini dibuat untuk keperluan edukasi dan verifikasi nomor OVO. Gunakan sesuai dengan ToS OVO dan peraturan yang berlaku.

## License 📄

MIT License - Feel free to use this project

## Support & Kontribusi 🤝

Punya pertanyaan atau saran? Buat issue atau pull request!

---

Made with ❤️ by Riski1610
