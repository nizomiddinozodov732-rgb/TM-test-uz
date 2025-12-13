# Vercel ga yuklash bo'yicha ko'rsatma

## Muammo
Vercel Flask ilovasini topa olmayapti, chunki u `app.py` yoki boshqa standart entry point faylini qidiradi.

## Yechim

1. **app.py** fayli yaratildi - bu Vercel uchun entry point
2. **vercel.json** konfiguratsiya fayli yaratildi
3. **.vercelignore** fayli yaratildi - keraksiz fayllarni yuklamaslik uchun

## Muhim eslatmalar

⚠️ **SQLite Database muammosi**: Vercel serverless funksiyalarida SQLite ishlamaydi, chunki fayl tizimi faqat o'qish uchun. 

### Yechimlar:
1. **Vercel Postgres** yoki **Vercel KV** ishlatish
2. **Supabase**, **PlanetScale** yoki boshqa cloud database ishlatish
3. **SQLite** o'rniga PostgreSQL yoki MySQL ga o'tish

## Yuklash qadamlari

1. GitHub repository ga kodlarni yuklang
2. Vercel dashboard ga kiring
3. "New Project" ni bosing
4. GitHub repository ni tanlang
5. Framework Preset: "Other" ni tanlang
6. Root Directory: "." (default)
7. Build Command: bo'sh qoldiring
8. Output Directory: bo'sh qoldiring
9. "Deploy" ni bosing

## Environment Variables

Agar database URL kerak bo'lsa, Vercel dashboard da Environment Variables qo'shing.

## API URL ni o'zgartirish

Frontend kodlarda `API_URL` ni Vercel URL ga o'zgartiring:
```javascript
const API_URL = 'https://your-project.vercel.app/api';
```

