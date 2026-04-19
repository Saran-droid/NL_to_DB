# Web Application Guide

This guide explains how to use the web-based Natural Language to SQL system with FastAPI backend and Streamlit frontend.

## Architecture

```
┌─────────────────┐
│   Streamlit     │  Port 8501
│   Frontend      │  (User Interface)
└────────┬────────┘
         │ HTTP Requests
         ▼
┌─────────────────┐
│   FastAPI       │  Port 8000
│   Backend       │  (API Server)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │  Port 5432
│   Database      │
└─────────────────┘
```

## Quick Start

### Option 1: Start Everything at Once (Recommended)

**Windows:**
```bash
start_all.bat
```

**Linux/Mac:**
```bash
chmod +x start_all.sh
./start_all.sh
```

This will start both backend and frontend servers automatically.

### Option 2: Start Servers Separately

**Terminal 1 - Backend:**
```bash
uv run start_backend.py
```

**Terminal 2 - Frontend:**
```bash
uv run start_frontend.py
```

## Accessing the Application

Once started, you can access:

- **Frontend (Streamlit):** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs (Interactive Swagger UI)
- **API Alternative Docs:** http://localhost:8000/redoc

## Features

### Frontend (Streamlit)

1. **Question Input**
   - Type your question in natural language
   - Click "Execute Query" to get results

2. **Example Questions**
   - Browse categorized examples in the sidebar
   - Click any example to auto-fill the question

3. **Query Results**
   - View results in a formatted table
   - Download results as CSV or JSON
   - See query statistics

4. **SQL Query Display**
   - View the generated SQL query
   - Copy SQL to clipboard
   - See explanations of what the query does

5. **Query History**
   - Recent queries are saved
   - Click to re-run previous queries

6. **Database Schema**
   - View all tables in the sidebar
   - Expand to see full schema details

7. **System Status**
   - Real-time health monitoring
   - Database connection status
   - API availability check

### Backend (FastAPI)

The backend provides a REST API with the following endpoints:

#### `GET /`
Health check endpoint
```json
{
  "status": "running",
  "database_connected": true,
  "groq_configured": true
}
```

#### `GET /health`
Detailed health check
```json
{
  "status": "healthy",
  "database_connected": true,
  "groq_configured": true
}
```

#### `GET /schema`
Get database schema
```json
{
  "schema": "Table: users\nColumns:\n...",
  "tables": ["users", "products", "orders"]
}
```

#### `POST /query`
Execute a natural language query

**Request:**
```json
{
  "question": "Show me all users older than 30",
  "explain": true
}
```

**Response:**
```json
{
  "question": "Show me all users older than 30",
  "sql_query": "SELECT * FROM users WHERE age > 30",
  "explanation": "This query selects all columns...",
  "results": [...],
  "row_count": 2,
  "success": true,
  "error": null
}
```

#### `GET /examples`
Get example questions organized by category

## Using the API Directly

### With curl

```bash
# Health check
curl http://localhost:8000/health

# Get schema
curl http://localhost:8000/schema

# Execute query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me all users", "explain": true}'
```

### With Python

```python
import requests

# Execute a query
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

### With JavaScript/Fetch

```javascript
// Execute a query
fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: 'Show me all users',
    explain: true
  })
})
.then(response => response.json())
.then(data => {
  console.log('SQL:', data.sql_query);
  console.log('Results:', data.results);
});
```

## Configuration

### Backend Configuration

The backend uses the same `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nl_to_sql_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

### Frontend Configuration

The frontend connects to the backend at `http://localhost:8000` by default. To change this, edit `frontend/app.py`:

```python
API_URL = "http://your-backend-url:8000"
```

## Deployment

### Development

Use the provided start scripts for local development with auto-reload enabled.

### Production

#### Backend (FastAPI)

```bash
# Install production server
uv pip install gunicorn

# Run with gunicorn
gunicorn backend.api:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

#### Frontend (Streamlit)

```bash
streamlit run frontend/app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true
```

### Docker Deployment

Create `Dockerfile.backend`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `Dockerfile.frontend`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - POSTGRES_HOST=db
      - POSTGRES_PORT=5432
      - POSTGRES_DB=nl_to_sql_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    depends_on:
      - db
  
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=nl_to_sql_db
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run with:
```bash
docker-compose up
```

## Troubleshooting

### Frontend can't connect to backend

**Error:** "API Offline" in the sidebar

**Solutions:**
1. Make sure backend is running: `uv run start_backend.py`
2. Check backend is accessible: `curl http://localhost:8000/health`
3. Verify no firewall is blocking port 8000

### Backend can't connect to database

**Error:** "Database Disconnected" in status

**Solutions:**
1. Check PostgreSQL is running
2. Verify credentials in `.env` file
3. Test connection: `uv run test_postgres.py`

### Port already in use

**Error:** "Address already in use"

**Solutions:**
1. Stop other services using ports 8000 or 8501
2. Change ports in start scripts
3. Kill existing processes:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <pid> /F
   
   # Linux/Mac
   lsof -ti:8000 | xargs kill -9
   ```

### CORS errors

**Error:** "CORS policy blocked"

**Solution:** The backend already has CORS enabled for all origins. If you still see errors, check your browser console for specific issues.

## Tips for Best Results

1. **Be Specific:** "Show users older than 30" is better than "show users"
2. **Use Table Names:** Reference actual tables from your schema
3. **Start Simple:** Test basic queries before complex ones
4. **Check Examples:** Use sidebar examples as templates
5. **Review SQL:** Always check the generated SQL to understand what's happening

## Security Considerations

### For Production:

1. **CORS:** Restrict allowed origins in `backend/api.py`:
   ```python
   allow_origins=["https://your-frontend-domain.com"]
   ```

2. **API Keys:** Never expose your `.env` file
3. **Rate Limiting:** Add rate limiting to prevent abuse
4. **Authentication:** Add user authentication if needed
5. **HTTPS:** Use HTTPS in production
6. **Database:** Use read-only database user for queries

## Next Steps

1. Customize the frontend styling in `frontend/app.py`
2. Add authentication to the API
3. Implement query caching
4. Add more visualization options
5. Create custom dashboards
6. Add export to more formats (Excel, PDF)

---

**Need Help?** Check the main README.md or run `uv run test_postgres.py` to diagnose issues.
