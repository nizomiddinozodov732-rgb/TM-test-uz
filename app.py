# Vercel uchun entry point
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from app_simple import app

# Vercel requires the app variable to be directly accessible
# @vercel/python automatically detects Flask apps and handles routing
# The Flask app will receive requests with the full path including /api prefix
__all__ = ['app']

# Ensure app is the handler
handler = app

