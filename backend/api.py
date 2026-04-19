"""FastAPI backend for Natural Language to SQL system."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nl_to_sql import NLToSQL
from database import Database


# Pydantic models
class QueryRequest(BaseModel):
    question: str
    explain: bool = True


class QueryResponse(BaseModel):
    question: str
    sql_query: str
    explanation: Optional[str] = None
    results: List[Dict[str, Any]]
    row_count: int
    success: bool
    error: Optional[str] = None


class SchemaResponse(BaseModel):
    schema: str
    tables: List[str]


class HealthResponse(BaseModel):
    status: str
    database_connected: bool
    groq_configured: bool


# Initialize FastAPI app
app = FastAPI(
    title="Natural Language to SQL API",
    description="Convert natural language questions to SQL queries and execute them",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for database and converter
db = None
converter = None
schema = None


@app.on_event("startup")
async def startup_event():
    """Initialize database connection and NL to SQL converter on startup."""
    global db, converter, schema
    
    try:
        # Initialize database
        db = Database()
        db.connect()
        
        # Check if tables exist, if not initialize
        try:
            schema = db.get_schema()
            if not schema or "Table:" not in schema:
                print("No tables found. Initializing database from schema.sql...")
                db.initialize_from_file()
                schema = db.get_schema()
        except Exception as e:
            print(f"Error getting schema: {e}")
            print("Attempting to initialize database...")
            db.initialize_from_file()
            schema = db.get_schema()
        
        # Initialize NL to SQL converter
        converter = NLToSQL()
        converter.set_schema(schema)
        
        print("✓ Backend initialized successfully")
        print(f"✓ Database connected")
        print(f"✓ Schema loaded")
        
    except Exception as e:
        print(f"✗ Startup error: {str(e)}")
        print("Please check your database configuration in .env file")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown."""
    global db
    if db:
        db.close()
        print("✓ Database connection closed")


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "database_connected": db is not None and db.connection is not None,
        "groq_configured": converter is not None
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check."""
    db_connected = False
    groq_configured = False
    
    try:
        if db and db.connection:
            # Test database connection
            db.execute_query("SELECT 1")
            db_connected = True
    except:
        pass
    
    try:
        if converter and converter.api_key:
            groq_configured = True
    except:
        pass
    
    return {
        "status": "healthy" if (db_connected and groq_configured) else "degraded",
        "database_connected": db_connected,
        "groq_configured": groq_configured
    }


@app.get("/schema", response_model=SchemaResponse)
async def get_schema():
    """Get database schema information."""
    if not db:
        raise HTTPException(status_code=503, detail="Database not initialized")
    
    try:
        schema_text = db.get_schema()
        
        # Extract table names
        tables = []
        for line in schema_text.split('\n'):
            if line.startswith('Table:'):
                table_name = line.replace('Table:', '').strip()
                tables.append(table_name)
        
        return {
            "schema": schema_text,
            "tables": tables
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting schema: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """
    Convert natural language question to SQL and execute it.
    
    Args:
        request: QueryRequest with question and optional explain flag
        
    Returns:
        QueryResponse with SQL query, results, and optional explanation
    """
    if not db or not converter:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        # Generate SQL query
        if request.explain:
            result = converter.generate_with_explanation(request.question)
            sql_query = result['query']
            explanation = result['explanation']
        else:
            sql_query = converter.generate_sql(request.question)
            explanation = None
        
        # Execute query
        results = db.execute_query(sql_query)
        
        return {
            "question": request.question,
            "sql_query": sql_query,
            "explanation": explanation,
            "results": results,
            "row_count": len(results),
            "success": True,
            "error": None
        }
        
    except Exception as e:
        return {
            "question": request.question,
            "sql_query": "",
            "explanation": None,
            "results": [],
            "row_count": 0,
            "success": False,
            "error": str(e)
        }


@app.get("/examples")
async def get_examples():
    """Get example questions users can ask."""
    return {
        "examples": [
            {
                "category": "Basic Queries",
                "questions": [
                    "Show me all users",
                    "List all products",
                    "How many orders are there?",
                    "What products are in stock?"
                ]
            },
            {
                "category": "Filtering",
                "questions": [
                    "Show me users older than 30",
                    "Find products in the Electronics category",
                    "List orders with quantity greater than 5",
                    "Show products with price less than 100"
                ]
            },
            {
                "category": "Aggregations",
                "questions": [
                    "What is the average age of users?",
                    "What are the total sales for each user?",
                    "Show me the most expensive product",
                    "Count products by category"
                ]
            },
            {
                "category": "Advanced",
                "questions": [
                    "Show me the top 3 users by total spending",
                    "Which products have low stock (less than 50)?",
                    "What is the average order value?",
                    "List users who have never placed an order"
                ]
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
