# Loyiha Qayta Tuzilishi - Qo'llanma

## ✅ Bajarilgan O'zgarishlar

### 1. Flask App Strukturasi
- ✅ `api/app.py` - Asosiy Flask app fayli yaratildi
- ✅ Flask app obyekti `app` nomi bilan yaratildi
- ✅ Barcha API endpointlar saqlanib qoldi

### 2. HTML Fayllar
- ✅ Barcha HTML fayllar `templates/` papkasiga ko'chirildi:
  - `Index.html`
  - `kirish.html`
  - `test_tanlov.html`
  - `test_yuklash.html`
  - `results.html`
  - `ishlash.html`

### 3. CSS Fayllar
- ✅ Barcha CSS fayllar `static/` papkasiga ko'chirildi:
  - `style.css`
  - `kirish.css`
  - `test_yuklash.css`
  - `ishlash.css`

### 4. Vercel Konfiguratsiyasi
- ✅ `vercel.json` yangilandi
- ✅ Barcha so'rovlar `api/app.py` ga yo'naltiriladi

### 5. HTML Fayllar Yangilandi
- ✅ CSS yo'llari `/static/` ga o'zgartirildi
- ✅ API URL'lar environment-aware qilindi (local va production)

## 📁 Yangi Struktura

```
Matematika test/
├── api/
│   └── app.py              # Flask asosiy fayli
├── templates/              # HTML fayllar
│   ├── Index.html
│   ├── kirish.html
│   ├── test_tanlov.html
│   ├── test_yuklash.html
│   ├── results.html
│   └── ishlash.html
├── static/                 # CSS va static fayllar
│   ├── style.css
│   ├── kirish.css
│   ├── test_yuklash.css
│   └── ishlash.css
├── models_simple.py        # Database modellari
├── vercel.json            # Vercel konfiguratsiyasi
└── requirements.txt       # Python paketlar
```

## 🔧 Vercel.json Konfiguratsiyasi

```json
{
  "version": 2,
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/api/app.py"
    }
  ]
}
```

**Izoh:** Barcha so'rovlar `api/app.py` ga yo'naltiriladi. Flask app ichida routing boshqariladi.

## 🚀 Local Development

Local ishlatish uchun:

```bash
cd api
python app.py
```

Yoki:

```bash
python api/app.py
```

Server `http://localhost:5000` da ishga tushadi.

## 📝 API Endpointlar

Barcha API endpointlar `/api/` prefiksi bilan ishlaydi:
- `POST /api/login`
- `GET /api/tests`
- `GET /api/tests/<test_id>`
- `POST /api/tests/create`
- `POST /api/tests/<test_id>/submit`
- `GET /api/results/<test_id>`
- va boshqalar...

## 🌐 HTML Sahifalar

Flask app quyidagi sahifalarni serve qiladi:
- `/` → `Index.html`
- `/kirish.html` → `kirish.html`
- `/test_tanlov.html` → `test_tanlov.html`
- `/test_yuklash.html` → `test_yuklash.html`
- `/results.html` → `results.html`
- `/ishlash.html` → `ishlash.html`

## 📦 Static Fayllar

CSS fayllar `/static/` orqali mavjud:
- `/static/style.css`
- `/static/kirish.css`
- `/static/test_yuklash.css`
- `/static/ishlash.css`

## ⚠️ Muhim Eslatmalar

1. **Database:** SQLite Vercel'da ishlamaydi. Cloud database ishlatish kerak.

2. **API URL:** HTML fayllarda API URL avtomatik ravishda environment ga moslashadi:
   - Local: `http://localhost:5000/api`
   - Production: `/api` (relative URL)

3. **Fayl Yo'llari:** 
   - HTML fayllar `templates/` da
   - CSS fayllar `static/` da
   - Flask app `api/app.py` da

## 🔄 Keyingi Qadamlar

1. **Deploy qilish:**
   ```bash
   git add .
   git commit -m "Restructure project for Vercel"
   git push
   ```

2. **Vercel'da test qilish:**
   - Barcha sahifalar ishlayotganini tekshiring
   - API endpointlarni test qiling
   - Static fayllar yuklanayotganini tekshiring

3. **Database migratsiya:**
   - SQLite'dan cloud database'ga o'tish
   - `models_simple.py` ni yangilash

## 📚 Qo'shimcha Ma'lumot

- Flask app `api/app.py` da joylashgan
- Templates `templates/` papkasida
- Static fayllar `static/` papkasida
- Vercel avtomatik ravishda `api/` papkasidagi Python fayllarni serverless function sifatida ishlatadi

