"""Natural language to SQL query generator using Groq."""
from groq import Groq
from typing import Optional
import os
from dotenv import load_dotenv


class NLToSQL:
    """Convert natural language queries to SQL using Groq's LLM."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        """Initialize the NL to SQL converter.
        
        Args:
            api_key: Groq API key (if not provided, will use GROQ_API_KEY env var)
            model: Model to use for generation
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found. Set it in .env file or pass as parameter.")
        
        self.client = Groq(api_key=self.api_key)
        self.model = model
        self.schema = None
    
    def set_schema(self, schema: str):
        """Set the database schema for context.
        
        Args:
            schema: String representation of database schema
        """
        self.schema = schema
    
    def generate_sql(self, natural_language_query: str) -> str:
        """Generate SQL query from natural language.
        
        Args:
            natural_language_query: User's question in natural language
            
        Returns:
            Generated SQL query
        """
        if not self.schema:
            raise ValueError("Schema not set. Call set_schema() first.")
        
        system_prompt = f"""You are a SQL query generator. Given a database schema and a natural language question, generate a valid SQL query.

Database Schema:
{self.schema}

Rules:
1. Generate ONLY the SQL query, no explanations or markdown
2. Use proper SQL syntax for PostgreSQL
3. Be precise and efficient
4. Use appropriate JOINs when needed
5. Return only SELECT queries for safety
6. Do not include semicolons at the end
7. Use proper column names from the schema
8. Use PostgreSQL-specific features when appropriate (e.g., LIMIT instead of TOP)"""

        user_prompt = f"Generate a SQL query for: {natural_language_query}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up the response (remove markdown code blocks if present)
            if sql_query.startswith("```sql"):
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            elif sql_query.startswith("```"):
                sql_query = sql_query.replace("```", "").strip()
            
            # Remove trailing semicolon if present
            sql_query = sql_query.rstrip(';')
            
            return sql_query
            
        except Exception as e:
            raise Exception(f"Error generating SQL: {str(e)}")
    
    def generate_with_explanation(self, natural_language_query: str) -> dict:
        """Generate SQL query with explanation.
        
        Args:
            natural_language_query: User's question in natural language
            
        Returns:
            Dictionary with 'query' and 'explanation' keys
        """
        if not self.schema:
            raise ValueError("Schema not set. Call set_schema() first.")
        
        system_prompt = f"""You are a SQL query generator. Given a database schema and a natural language question, generate a valid SQL query with explanation.

Database Schema:
{self.schema}

Respond in this exact format:
QUERY: <sql query here>
EXPLANATION: <brief explanation here>"""

        user_prompt = f"Generate a SQL query for: {natural_language_query}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse the response
            query = ""
            explanation = ""
            
            if "QUERY:" in content and "EXPLANATION:" in content:
                parts = content.split("EXPLANATION:")
                query = parts[0].replace("QUERY:", "").strip()
                explanation = parts[1].strip()
                
                # Clean up query
                if query.startswith("```sql"):
                    query = query.replace("```sql", "").replace("```", "").strip()
                elif query.startswith("```"):
                    query = query.replace("```", "").strip()
                query = query.rstrip(';')
            else:
                query = content
                explanation = "No explanation provided"
            
            return {
                "query": query,
                "explanation": explanation
            }
            
        except Exception as e:
            raise Exception(f"Error generating SQL: {str(e)}")
