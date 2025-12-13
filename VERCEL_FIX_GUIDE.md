# Vercel NOT_FOUND Error - Fix Guide

## 🔍 Root Cause Analysis

### What Was Happening vs. What Should Happen

**What the code was doing:**
- `vercel.json` was routing `/api/(.*)` requests to `app.py`
- Flask app had routes defined like `/api/login`, `/api/tests`, etc.
- Static files were being routed, but route order might have caused conflicts

**What it needed to do:**
- Properly route API requests to the Flask serverless function
- Ensure static files are served before catch-all routes
- Preserve the full path (`/api/...`) when passing to Flask

**What triggered the NOT_FOUND error:**
1. **Route matching issues**: Vercel's routing system might not have been correctly matching requests to the Flask app
2. **Path preservation**: When routing `/api/tests` to `app.py`, Flask needs to receive the full path
3. **Route order**: Static file routes need to be checked before catch-all routes

**The misconception:**
- Assuming Vercel would automatically handle Flask routing without proper configuration
- Not understanding that route order matters in Vercel's routing system
- Not realizing that static files need explicit routing before catch-all patterns

## ✅ The Fix

### 1. Updated `vercel.json`

**Changes made:**
- Ensured API routes are matched first: `/api/(.*)` → `app.py`
- Added proper static file routing with cache headers
- Fixed route order: API → Static files → Root → Catch-all

**Key improvements:**
```json
{
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "app.py"  // Routes all /api/* to Flask app
    },
    {
      "src": "/(.*\\.(html|css|js|...))",
      "dest": "/$1",  // Serves static files
      "headers": {
        "Cache-Control": "public, max-age=31536000, immutable"
      }
    },
    {
      "src": "/",
      "dest": "/Index.html"  // Root path
    },
    {
      "src": "/(.*)",
      "dest": "/Index.html"  // Catch-all for SPA routing
    }
  ]
}
```

### 2. Enhanced Flask App

**Added:**
- Root route handler (`/`) for health checks
- API root route (`/api`) for API discovery
- Better error handling

### 3. Static File Configuration

- Added cache headers for static assets
- Ensured static files are served before catch-all routes

## 📚 Understanding the Concept

### Why This Error Exists

The Vercel NOT_FOUND error exists because:
1. **Serverless Architecture**: Vercel uses serverless functions, not traditional servers
2. **Explicit Routing**: Every request must be explicitly routed to a handler
3. **Path Matching**: Routes are matched in order, and the first match wins

### The Correct Mental Model

Think of Vercel routing like a switchboard:
```
Request → Route Matcher → Handler
         ↓
    [Check routes in order]
         ↓
    [First match wins]
         ↓
    [Route to handler]
```

**Key principles:**
1. **Route order matters**: More specific routes should come first
2. **Pattern matching**: Use regex patterns to match request paths
3. **Handler assignment**: Each route must have a destination handler
4. **Static vs Dynamic**: Static files need explicit routing

### How This Fits into Vercel's Framework

Vercel's routing system:
- **Builds**: Define what to build (Python, Node.js, etc.)
- **Routes**: Define how to route requests
- **Rewrites**: Modify request paths (optional)
- **Headers**: Add response headers (optional)

For Flask apps:
- `@vercel/python` builder detects Flask apps automatically
- Routes API requests to the Flask app
- Flask handles internal routing based on `@app.route()` decorators

## ⚠️ Warning Signs to Watch For

### What to Look Out For

1. **Route Order Issues**
   - ❌ Catch-all routes (`/(.*)`) before specific routes
   - ✅ Specific routes (`/api/(.*)`) before catch-all

2. **Missing Static File Routes**
   - ❌ No explicit routing for `.html`, `.css`, `.js` files
   - ✅ Explicit static file routing with proper extensions

3. **Path Stripping**
   - ❌ Routing `/api/(.*)` to `/api/$1` (might strip path)
   - ✅ Routing `/api/(.*)` directly to handler

4. **Build Configuration**
   - ❌ Missing `builds` section in `vercel.json`
   - ✅ Proper `builds` with correct `src` and `use` fields

### Code Smells

```json
// ❌ BAD: Catch-all before specific routes
{
  "routes": [
    { "src": "/(.*)", "dest": "/index.html" },
    { "src": "/api/(.*)", "dest": "app.py" }
  ]
}

// ✅ GOOD: Specific routes first
{
  "routes": [
    { "src": "/api/(.*)", "dest": "app.py" },
    { "src": "/(.*)", "dest": "/index.html" }
  ]
}
```

### Similar Mistakes to Avoid

1. **Forgetting static file routing**
   - Always route static assets explicitly
   - Use proper file extensions in patterns

2. **Incorrect route patterns**
   - Use `(.*)` for catch-all, not `*`
   - Escape special regex characters

3. **Missing error handlers**
   - Add 404 handlers in Flask
   - Add error routes in vercel.json if needed

## 🔄 Alternative Approaches

### Approach 1: Current (Single Flask App)
**Pros:**
- Simple structure
- All routes in one place
- Easy to maintain

**Cons:**
- Single serverless function (cold starts)
- All routes bundled together

**Best for:** Small to medium apps

### Approach 2: API Directory Structure
**Structure:**
```
api/
  login.py
  tests.py
  results.py
```

**Pros:**
- Individual serverless functions
- Better cold start performance
- Independent scaling

**Cons:**
- More files to manage
- Code duplication possible
- More complex routing

**Best for:** Large apps with many endpoints

### Approach 3: Hybrid (Current + API Directory)
**Structure:**
```
app.py (main Flask app)
api/
  [specific endpoints as separate functions]
```

**Pros:**
- Flexibility
- Can optimize hot paths

**Cons:**
- More complex setup
- Mixed patterns

**Best for:** Apps needing optimization

## 🚀 Deployment Checklist

- [x] `vercel.json` has correct route order
- [x] Flask app has root and `/api` routes
- [x] Static files are properly routed
- [ ] Update API URLs in HTML files (see below)
- [ ] Configure database (SQLite won't work on Vercel!)
- [ ] Set environment variables if needed
- [ ] Test all API endpoints after deployment

## 📝 Next Steps

### 1. Update API URLs in HTML Files

All HTML files currently use:
```javascript
const API_URL = 'http://localhost:5000/api';
```

**For Vercel deployment, change to:**
```javascript
// Auto-detect environment
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000/api'
  : `${window.location.origin}/api`;
```

Or use your Vercel URL:
```javascript
const API_URL = 'https://your-project.vercel.app/api';
```

### 2. Database Migration

⚠️ **CRITICAL**: SQLite doesn't work on Vercel (read-only filesystem)!

**Options:**
1. **Vercel Postgres** (recommended)
2. **Supabase** (free tier available)
3. **PlanetScale** (MySQL compatible)
4. **MongoDB Atlas** (NoSQL option)

### 3. Environment Variables

If using a cloud database, add connection strings in Vercel Dashboard:
- Settings → Environment Variables
- Add `DATABASE_URL` or similar

## 🎓 Key Takeaways

1. **Route order is critical** - Specific routes before catch-all
2. **Static files need explicit routing** - Don't rely on defaults
3. **Flask apps work with `@vercel/python`** - But routing must be correct
4. **SQLite won't work** - Use cloud databases
5. **Test locally first** - Use `vercel dev` for local testing

## 🔗 Additional Resources

- [Vercel Routing Documentation](https://vercel.com/docs/concepts/projects/project-configuration#routes)
- [Vercel Python Documentation](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [Flask on Vercel Guide](https://vercel.com/guides/deploying-flask-with-vercel)

