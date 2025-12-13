# Matematika Test Backend

Bu loyiha matematika test tizimi uchun backend API hisoblanadi.

## O'rnatish

1. Python paketlarini o'rnating:
```bash
pip install -r requirements.txt
```

## Ishga tushirish

Backend serverni ishga tushirish:
```bash
python app.py
```

**Eslatma:** Agar `app.py` ishlamasa, `app_simple.py` faylini ishlatishingiz mumkin:
```bash
python app_simple.py
```

Server `http://localhost:5000` manzilida ishga tushadi.

## API Endpointlar

### 1. Foydalanuvchi kirish
**POST** `/api/login`
```json
{
  "name": "Ozodov Nizomjon",
  "id": "123456"
}
```

### 2. Barcha testlarni olish
**GET** `/api/tests`

### 3. Bitta testni olish (savollar bilan)
**GET** `/api/tests/<test_id>`

### 4. Yangi test yaratish
**POST** `/api/tests/create`
```json
{
  "name": "Matematika test",
  "questions": [
    {
      "question_text": "16 ning ildizi",
      "correct_answer": "A",
      "answers": [
        {"variant": "A", "text": "4"},
        {"variant": "B", "text": "2"},
        {"variant": "C", "text": "8"},
        {"variant": "D", "text": "6"}
      ]
    }
  ]
}
```

### 5. Test javoblarini yuborish
**POST** `/api/tests/<test_id>/submit`
```json
{
  "user_id": "123456",
  "answers": [
    {"question_id": 1, "answer": "A"},
    {"question_id": 2, "answer": "B"}
  ]
}
```

### 6. Test natijalarini olish
**GET** `/api/results/<test_id>`

### 7. Foydalanuvchi natijalarini olish
**GET** `/api/results/user/<user_id>`

### 8. Bitta natijani olish
**GET** `/api/results/<result_id>`

## Database

SQLite database fayli `matematika_test.db` nomi bilan yaratiladi.

## Eslatma

Frontend HTML fayllarini backend API bilan bog'lash uchun JavaScript kod qo'shishingiz kerak bo'ladi.

