# PostgreSQL Setup for LMS Profile Storage

## Free Online PostgreSQL Options:
1. **Supabase** (Recommended) - https://supabase.com
   - Free tier: 2GB storage, unlimited API calls
   - Easy setup, includes dashboard

2. **Railway** - https://railway.app
   - Free tier: $5 credit/month

3. **Render** - https://render.com
   - Free tier PostgreSQL available

## Steps to Set Up Supabase:

1. Go to https://supabase.com and sign up
2. Create a new project
3. Get your connection string from Settings > Database
4. Update config.py with the PostgreSQL credentials

## Connection String Format:
```
postgresql://username:password@host:port/database
```

## Or use MySQL Online:
- JawsDB (https://www.jawsdb.com) - Free tier for MySQL
- ClearDB (https://www.cleardb.com) - MySQL hosting
