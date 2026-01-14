# Vercel uchun entry point
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app_simple import app
except ImportError as e:
    print(f"Import xatolik: {e}")
    print("Iltimos, Flask va Flask-CORS kutubxonalarini o'rnating:")
    print("pip install Flask Flask-CORS")
    raise

# Vercel requires the app variable to be directly accessible
# @vercel/python automatically detects Flask apps and handles routing
# The Flask app will receive requests with the full path including /api prefix
__all__ = ['app']

# Ensure app is the handler
handler = app

# Local development entrypoint
if __name__ == "__main__":
    print("=" * 50)
    print("Matematika Test Backend Server")
    print("=" * 50)
    print("Server ishga tushmoqda...")
    print("URL: http://localhost:5000")
    print("API Base URL: http://localhost:5000/api")
    print("Asosiy sahifa: http://localhost:5000/")
    print("=" * 50)
    try:
        app.run(debug=True, host="0.0.0.0", port=5000)
    except Exception as e:
        print(f"Server ishga tushirishda xatolik: {e}")
        print("Iltimos, Flask va Flask-CORS kutubxonalarini o'rnating:")
        print("pip install Flask Flask-CORS")
#         raise
# from flask import Flask
# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "OK"
