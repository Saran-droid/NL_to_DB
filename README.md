# Natural Language to SQL

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.56+-red.svg)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Transform natural language questions into SQL queries using AI, then execute them against your PostgreSQL database.

## ✨ Features

- 🤖 **AI-Powered** - Uses Groq's llama-3.3-70b-versatile model
- 🌐 **Web Interface** - Beautiful Streamlit UI for easy interaction
- 🚀 **REST API** - FastAPI backend for integration with other applications
- 💻 **CLI Tool** - Command-line interface for terminal users
- 📊 **Data Export** - Download results as CSV or JSON
- 🔒 **Safe** - Only generates SELECT queries (no data modification)
- 📚 **Examples** - Pre-built question library to get started
- 🔍 **Schema Aware** - Automatically understands your database structure

## 🎯 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Groq API key ([Get one free](https://console.groq.com/))

### Installation

```bash
# Clone the repository
git clone https://github.com/Saran-droid/NL_to_DB.git
cd NL_to_DB

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Running the Application

**Option 1: Web Application (Recommended)**

```bash
# Windows
start_all.bat

# Linux/Mac
chmod +x start_all.sh
./start_all.sh
```

Then open http://localhost:8501 in your browser.

**Option 2: Using the run script**

```bash
python run.py all        # Start both backend and frontend
python run.py backend    # Start only the API server
python run.py frontend   # Start only the web UI
python run.py cli        # Run command-line interface
```

**Option 3: Command Line Interface**

```bash
python -m nl_to_sql
```

## 📖 Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running in 5 minutes
- **[Web App Guide](docs/WEB_APP_GUIDE.md)** - Complete guide for the web application
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when backend is running)

## 🏗️ Project Structure

```
nl-to-sql/
├── src/
│   └── nl_to_sql/          # Main package
│       ├── __init__.py     # Package initialization
│       ├── api.py          # FastAPI backend
│       ├── cli.py          # Command-line interface
│       ├── converter.py    # NL to SQL conversion logic
│       ├── database.py     # Database connection & queries
│       └── frontend.py     # Streamlit web interface
├── scripts/                # Utility scripts
│   ├── start_backend.py    # Start API server
│   └── start_frontend.py   # Start web UI
├── tests/                  # Test files
│   └── test_connection.py  # Database connection tests
├── docs/                   # Documentation
│   ├── QUICK_START.md
│   └── WEB_APP_GUIDE.md
├── schema.sql              # Database schema
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── run.py                 # Main entry point
├── .env.example           # Environment template
└── README.md              # This file
```

## 🔧 Configuration

Create a `.env` file with your credentials:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nl_to_sql_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
```

### PostgreSQL Setup

**Docker (Fastest)**
```bash
docker run --name postgres-nlsql \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=nl_to_sql_db \
  -p 5432:5432 \
  -d postgres:15
```

**Cloud (Easiest)**
- [Neon](https://neon.tech/) - Serverless PostgreSQL
- [Supabase](https://supabase.com/) - PostgreSQL + APIs
- [ElephantSQL](https://elephantsql.com/) - Managed PostgreSQL

## 💡 Usage Examples

### Web Interface

1. Start the application: `python run.py all`
2. Open http://localhost:8501
3. Type your question: "Show me all users older than 30"
4. View the generated SQL and results
5. Download results as CSV or JSON

### REST API

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={
        "question": "Show me all users older than 30",
        "explain": True
    }
)

result = response.json()
print(f"SQL: {result['sql_query']}")
print(f"Results: {result['results']}")
```

### Command Line

```bash
python -m nl_to_sql

Your question: Show me all users older than 30
```

### As a Python Package

```python
from nl_to_sql import NLToSQL, Database

# Initialize
db = Database()
db.connect()

converter = NLToSQL()
converter.set_schema(db.get_schema())

# Generate and execute
sql = converter.generate_sql("Show me all users")
results = db.execute_query(sql)
```

## 🧪 Testing

```bash
# Test database connection
python tests/test_connection.py

# Run all tests
pytest tests/
```

## 🚀 Deployment

### Docker

```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Production

See [docs/WEB_APP_GUIDE.md](docs/WEB_APP_GUIDE.md) for detailed deployment instructions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for the amazing LLM API
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Streamlit](https://streamlit.io/) for the frontend framework
- [PostgreSQL](https://www.postgresql.org/) for the database

## 📧 Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/Saran-droid/NL_to_DB/issues)
- 💬 [Discussions](https://github.com/Saran-droid/NL_to_DB/discussions)

---

Made with ❤️ by the Natural Language to SQL team
