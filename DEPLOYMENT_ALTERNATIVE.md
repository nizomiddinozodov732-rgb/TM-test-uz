# Alternative Deployment Approach - API Directory Structure

If the current `builds` approach doesn't work, use this more reliable method:

## 📁 Directory Structure

```
your-project/
├── api/
│   └── index.py          # Flask app entry point
├── app_simple.py          # Your Flask app (keep as is)
├── models_simple.py       # Database models
├── vercel.json           # Updated config
├── Index.html
└── ... (other files)
```

## 🔧 Steps to Implement

### 1. Create `api/` Directory

```bash
mkdir api
```

### 2. Create `api/index.py`

```python
# api/index.py
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app_simple import app

# Vercel requires the app variable
__all__ = ['app']
handler = app
```

### 3. Update `vercel.json`

```json
{
  "version": 2,
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api"
    },
    {
      "src": "/(.*\\.(html|css|js|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot))",
      "dest": "/$1",
      "headers": {
        "Cache-Control": "public, max-age=31536000, immutable"
      }
    },
    {
      "src": "/",
      "dest": "/Index.html"
    },
    {
      "src": "/(.*)",
      "dest": "/Index.html"
    }
  ]
}
```

**Note:** No `builds` section needed - Vercel auto-detects Python files in `api/`

### 4. Keep `app.py` (Optional)

You can keep `app.py` for local development, or remove it if using this approach.

## ✅ Advantages

- ✅ More reliable (Vercel's recommended approach)
- ✅ Auto-detection (no `builds` config needed)
- ✅ Better error messages
- ✅ Easier debugging

## 🚀 Deploy

1. Commit changes
2. Push to GitHub
3. Vercel will auto-deploy
4. Test endpoints

