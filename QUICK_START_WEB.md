# Quick Start - Web Application

Get your Natural Language to SQL web app running in 5 minutes!

## ⚡ Super Quick Start

```bash
# 1. Navigate to project
cd nl-to-sql

# 2. Create .env file
copy .env.example .env

# 3. Edit .env with your credentials
# - Add your Groq API key
# - Add your PostgreSQL credentials

# 4. Start everything
start_all.bat  # Windows
./start_all.sh # Linux/Mac
```

That's it! Open http://localhost:8501 in your browser.

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] PostgreSQL running (local, Docker, or cloud)
- [ ] Database `nl_to_sql_db` created
- [ ] Groq API key from https://console.groq.com/
- [ ] `.env` file configured

## 🚀 Step-by-Step Guide

### Step 1: Configure Environment (2 minutes)

Create `.env` file:
```bash
copy .env.example .env
```

Edit `.env`:
```env
GROQ_API_KEY=gsk_your_actual_key_here

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nl_to_sql_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

### Step 2: Start the Servers (30 seconds)

**Windows:**
```bash
start_all.bat
```

**Linux/Mac:**
```bash
chmod +x start_all.sh
./start_all.sh
```

This starts:
- ✅ Backend API on port 8000
- ✅ Frontend UI on port 8501

### Step 3: Open the Web App

Your browser should open automatically, or go to:
- **Frontend:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs

## 🎨 Using the Web Interface

### Main Features

1. **Question Input Box**
   - Type your question in plain English
   - Example: "Show me all users older than 30"

2. **Example Questions (Sidebar)**
   - Click any example to try it
   - Organized by difficulty level

3. **Results Display**
   - View results in a table
   - Download as CSV or JSON
   - See row count and statistics

4. **SQL Query Display**
   - See the generated SQL
   - Copy to clipboard
   - Read explanation of what it does

5. **Query History**
   - Recent queries saved automatically
   - Click to re-run

6. **Database Schema (Sidebar)**
   - View all tables
   - Expand to see columns and types

### Example Workflow

1. **Click an example:** "Show me all users"
2. **Review the question** in the input box
3. **Click "Execute Query"**
4. **View results:**
   - See the SQL query generated
   - Read the explanation
   - View results in table format
5. **Download results** if needed (CSV/JSON)

## 🔧 Alternative: Start Servers Separately

If you prefer more control:

**Terminal 1 - Backend:**
```bash
uv run start_backend.py
```
Wait for: "Application startup complete"

**Terminal 2 - Frontend:**
```bash
uv run start_frontend.py
```
Wait for: "You can now view your Streamlit app in your browser"

## 🌐 Accessing the Services

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:8501 | Streamlit web interface |
| Backend API | http://localhost:8000 | FastAPI REST API |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| API Redoc | http://localhost:8000/redoc | Alternative API docs |

## 💡 Try These Questions

Once the app is running, try asking:

### Basic
- "Show me all users"
- "List all products"
- "How many orders are there?"

### Filtering
- "Show me users older than 30"
- "Find products in the Electronics category"
- "List orders with quantity greater than 5"

### Aggregations
- "What is the average age of users?"
- "What are the total sales for each user?"
- "Show me the most expensive product"

### Advanced
- "Show me the top 3 users by total spending"
- "Which products have low stock (less than 50)?"
- "What is the average order value?"

## 🐛 Troubleshooting

### Frontend shows "API Offline"

**Problem:** Frontend can't connect to backend

**Solutions:**
1. Check backend is running: http://localhost:8000/health
2. Restart backend: `uv run start_backend.py`
3. Check no firewall blocking port 8000

### Backend shows database errors

**Problem:** Can't connect to PostgreSQL

**Solutions:**
1. Check PostgreSQL is running
2. Verify credentials in `.env`
3. Test connection: `uv run test_postgres.py`
4. Create database: `psql -U postgres -c "CREATE DATABASE nl_to_sql_db;"`

### Port already in use

**Problem:** "Address already in use"

**Solutions:**
```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# Linux/Mac - Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Browser doesn't open automatically

**Solution:** Manually open http://localhost:8501

## 🎯 What's Next?

Once you're comfortable with the basics:

1. **Explore the API**
   - Visit http://localhost:8000/docs
   - Try API endpoints directly
   - Use in your own applications

2. **Customize Your Schema**
   - Edit `schema.sql` with your tables
   - Restart the backend
   - Ask questions about your data

3. **Integrate with Your App**
   - Use the REST API from any language
   - See WEB_APP_GUIDE.md for examples

4. **Deploy to Production**
   - See WEB_APP_GUIDE.md for deployment options
   - Use Docker for easy deployment

## 📚 More Resources

- **[WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)** - Complete web app documentation
- **[README.md](README.md)** - Full project documentation
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Detailed setup guide

## 🆘 Still Having Issues?

1. Run the test script: `uv run test_postgres.py`
2. Check all prerequisites are met
3. Review error messages in terminal
4. Verify `.env` file is configured correctly

---

**Estimated Setup Time:** 5 minutes

**Ready?** Let's go! 🚀
