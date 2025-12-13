# Vercel uchun entry point
from app_simple import app

# Vercel requires the app variable to be directly accessible
# @vercel/python automatically detects Flask apps and handles routing
__all__ = ['app']

