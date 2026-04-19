# Natural Language to SQL Query System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.56+-red.svg)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python application that converts natural language questions into SQL queries using Groq's llama-3.3-70b-versatile model and PostgreSQL.

## 🌟 Features

- 🤖 Natural language to SQL conversion using Groq AI
- 🌐 **Web Interface** with Streamlit frontend
- 🚀 **REST API** with FastAPI backend
- 📊 Automatic database schema detection
- 🔍 Query execution and result display
- 💡 Query explanations
- 📥 Export results (CSV, JSON)
- 🐘 PostgreSQL database with sample data
- 🔒 Safe query generation (SELECT only)

## 🎯 Two Ways to Use

### 1. Web Application (Recommended)

Beautiful web interface with:
- Interactive query builder
- Real-time results
- Example questions
- Query history
- Download results

**Start the web app:**
```bash
# Windows
start_all.bat

# Linux/Mac
./start_all.sh
```

Then open http://localhost:8501 in your browser.

### 2. Command Line Interface

Traditional CLI for terminal users:
```bash
uv run main.py
```

## Prerequisites

- Python 3.8+ (managed by uv)
- PostgreSQL 12+ (local, Docker, or cloud)
- Groq API key (free at https://console.groq.com/)

### Quick PostgreSQL Setup

**Option 1: Docker (Fastest)**
```bash
docker run --name postgres-nlsql -e POSTGRES_PASSWORD=password -e POSTGRES_DB=nl_to_sql_db -p 5432:5432 -d postgres:15
```

**Option 2: Cloud (Easiest)**
- [Neon](https://neon.tech/) - Serverless PostgreSQL (free tier)
- [Supabase](https://supabase.com/) - PostgreSQL + APIs (free tier)
- [ElephantSQL](https://elephantsql.com/) - Managed PostgreSQL (free tier)

**Option 3: Local**
- Download from https://www.postgresql.org/download/
- Create database: `CREATE DATABASE nl_to_sql_db;`

## Setup

### 1. Install uv (if not already installed)

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

### 2. Set up PostgreSQL

**Quick options:**
- **Docker:** `docker run --name postgres-nlsql -e POSTGRES_PASSWORD=password -e POSTGRES_DB=nl_to_sql_db -p 5432:5432 -d postgres:15`
- **Cloud:** Use [Neon](https://neon.tech/), [Supabase](https://supabase.com/), or [ElephantSQL](https://elephantsql.com/) free tier
- **Local:** Install from https://www.postgresql.org/download/ and create database

Create the database:
```sql
CREATE DATABASE nl_to_sql_db;
```

### 3. Install dependencies

```bash
cd nl-to-sql
uv venv
.venv\Scripts\activate  # On Windows
uv pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file from the example:

```bash
copy .env.example .env
```

Edit `.env` with your credentials:

```env
GROQ_API_KEY=your_actual_groq_api_key_here

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nl_to_sql_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
```

Get your Groq API key from: https://console.groq.com/keys

### 5. Start the application

**Option A: Web Application (Recommended)**

```bash
# Windows
start_all.bat

# Linux/Mac  
chmod +x start_all.sh
./start_all.sh
```

Then open http://localhost:8501 in your browser.

**Option B: Command Line Interface**

```bash
uv run main.py
```

The database will be automatically initialized with sample data on first run.

## 📖 Documentation

- **[QUICK_START_WEB.md](QUICK_START_WEB.md)** - Get the web app running in 5 minutes
- **[WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)** - Complete guide for the web application and API

## Troubleshooting

### "GROQ_API_KEY not found"
Create a `.env` file with your API key from https://console.groq.com/

### "API Offline" in web interface
Start the backend: `uv run start_backend.py`

### Database connection errors
1. Check PostgreSQL is running
2. Verify credentials in `.env`
3. Test connection: `uv run test_postgres.py`
4. Create database: `psql -U postgres -c "CREATE DATABASE nl_to_sql_db;"`

### "Module not found"
Install dependencies: `uv pip install -r requirements.txt`

## Usage

### Web Application

1. **Start the servers:**
   ```bash
   start_all.bat  # Windows
   ./start_all.sh # Linux/Mac
   ```

2. **Open your browser:**
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

3. **Ask questions:**
   - Type your question in natural language
   - Click example questions from the sidebar
   - View results, SQL queries, and explanations
   - Download results as CSV or JSON

### Command Line Interface

```bash
uv run main.py
```

### API Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={"question": "Show me all users", "explain": True}
)

result = response.json()
print(result["sql_query"])
print(result["results"])
```

### Example queries

Try asking questions like:

- "Show me all users"
- "What are the total sales for each user?"
- "Find all products in the Electronics category"
- "Show me orders with quantity greater than 5"
- "List users older than 30"
- "What is the average price of products?"

### Using as a library

```python
from nl_to_sql import NLToSQL
from database import Database

# Initialize
db = Database()
db.connect()
schema = db.get_schema()

# Create converter
converter = NLToSQL()
converter.set_schema(schema)

# Generate SQL
query = converter.generate_sql("Show me all users")
print(query)

# Execute
results = db.execute_query(query)
print(results)
```

## Project Structure

```
nl-to-sql/
├── backend/
│   └── api.py               # FastAPI REST API server
├── frontend/
│   └── app.py               # Streamlit web interface
├── .env.example             # Environment variables template
├── .env                     # Your API keys (create this)
├── requirements.txt         # Python dependencies
├── schema.sql              # PostgreSQL schema and sample data
├── nl_to_sql.py            # NL to SQL converter class
├── database.py             # PostgreSQL connection and utilities
├── main.py                 # CLI application
├── test_postgres.py        # PostgreSQL connection test
├── start_all.bat           # Windows: Start both servers
├── start_all.sh            # Linux/Mac: Start both servers
├── start_backend.py        # Start FastAPI backend
├── start_frontend.py       # Start Streamlit frontend
├── README.md               # This file
├── WEB_APP_GUIDE.md        # Web application documentation
├── GETTING_STARTED.md      # Step-by-step setup guide
└── setup_postgres.md       # PostgreSQL setup instructions
```

## Customization

### Using your own database schema

1. Edit `schema.sql` with your PostgreSQL table definitions
2. Drop and recreate the database, or run the schema manually
3. Run `uv run main.py` to use the new schema

### Connecting to existing PostgreSQL database

If you have an existing database, just update the `.env` file with your connection details. The application will read the schema automatically without modifying your data.

### Changing the model

You can use different Groq models by modifying the initialization:

```python
converter = NLToSQL(model="llama-3.1-70b-versatile")
```

Available models:
- `llama-3.3-70b-versatile` (default, recommended)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`

## Safety Features

- Only SELECT queries are generated (no INSERT, UPDATE, DELETE)
- Schema validation before query generation
- Error handling with detailed messages

## Troubleshooting

### "GROQ_API_KEY not found"
Create a `.env` file with your API key from https://console.groq.com/

### "API Offline" in web interface
Start the backend: `uv run start_backend.py`

### Database connection errors
1. Check PostgreSQL is running
2. Verify credentials in `.env`
3. Test connection: `uv run test_postgres.py`
4. Create database: `psql -U postgres -c "CREATE DATABASE nl_to_sql_db;"`

### "Module not found"
Install dependencies: `uv pip install -r requirements.txt`

## License

MIT License - feel free to use and modify as needed.
