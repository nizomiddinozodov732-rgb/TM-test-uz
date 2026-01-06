# Kutubxonalarni O'rnatish

## Python kutubxonalarini o'rnatish

Terminal yoki Command Prompt ni oching va quyidagi buyruqlarni bajaring:

```bash
cd "E:\HTML va CSS\Matematika test"
pip install -r requirements.txt
```

Yoki alohida o'rnatish:

```bash
pip install Flask>=2.3.0
pip install Flask-CORS>=4.0.0
```

## Tekshirish

Kutubxonalar o'rnatilganini tekshirish:

```bash
python -c "import flask; import flask_cors; print('Flask:', flask.__version__); print('Flask-CORS:', flask_cors.__version__)"
```

## Muammo bo'lsa

Agar `pip` topilmasa:
1. Python o'rnatilganligini tekshiring: `python --version`
2. Yoki `python3` yoki `py` ishlatib ko'ring: `py -m pip install -r requirements.txt`






