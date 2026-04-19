"""Database connection and schema management."""
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any
import os
from dotenv import load_dotenv


class Database:
    """Handle database connections and queries."""
    
    def __init__(self, connection_string: str = None):
        """Initialize database connection.
        
        Args:
            connection_string: PostgreSQL connection string (optional)
                             If not provided, will use environment variables
        """
        load_dotenv()
        
        if connection_string:
            self.connection_string = connection_string
        else:
            # Build connection string from environment variables
            host = os.getenv("POSTGRES_HOST", "localhost")
            port = os.getenv("POSTGRES_PORT", "5432")
            database = os.getenv("POSTGRES_DB", "nl_to_sql_db")
            user = os.getenv("POSTGRES_USER", "postgres")
            password = os.getenv("POSTGRES_PASSWORD", "")
            
            self.connection_string = f"host={host} port={port} dbname={database} user={user} password={password}"
        
        self.connection = None
    
    def connect(self):
        """Create database connection."""
        try:
            self.connection = psycopg2.connect(
                self.connection_string,
                cursor_factory=RealDictCursor
            )
            self.connection.autocommit = False
            return self.connection
        except psycopg2.Error as e:
            raise Exception(f"Database connection error: {str(e)}")
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            # Fetch results
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            results = [dict(row) for row in rows]
            
            return results
        except psycopg2.Error as e:
            self.connection.rollback()
            raise Exception(f"Query execution error: {str(e)}")
    
    def get_schema(self) -> str:
        """Get database schema as a string."""
        cursor = self.connection.cursor()
        
        # Get all tables in public schema
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        schema_info = []
        for table in tables:
            table_name = table['table_name']
            
            # Get column information
            cursor.execute("""
                SELECT 
                    column_name,
                    data_type,
                    character_maximum_length,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = 'public' 
                AND table_name = %s
                ORDER BY ordinal_position;
            """, (table_name,))
            columns = cursor.fetchall()
            
            # Get primary key information
            cursor.execute("""
                SELECT a.attname
                FROM pg_index i
                JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
                WHERE i.indrelid = %s::regclass AND i.indisprimary;
            """, (table_name,))
            pk_columns = [row['attname'] for row in cursor.fetchall()]
            
            # Get foreign key information
            cursor.execute("""
                SELECT
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                    AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND tc.table_name = %s;
            """, (table_name,))
            fk_info = {row['column_name']: (row['foreign_table_name'], row['foreign_column_name']) 
                      for row in cursor.fetchall()}
            
            schema_info.append(f"\nTable: {table_name}")
            schema_info.append("Columns:")
            for col in columns:
                col_name = col['column_name']
                data_type = col['data_type']
                
                # Add length for varchar/char types
                if col['character_maximum_length']:
                    data_type += f"({col['character_maximum_length']})"
                
                constraints = []
                if col_name in pk_columns:
                    constraints.append("PRIMARY KEY")
                if col['is_nullable'] == 'NO':
                    constraints.append("NOT NULL")
                if col_name in fk_info:
                    fk_table, fk_col = fk_info[col_name]
                    constraints.append(f"FOREIGN KEY -> {fk_table}({fk_col})")
                
                constraint_str = " " + " ".join(constraints) if constraints else ""
                schema_info.append(f"  - {col_name} ({data_type}){constraint_str}")
        
        return "\n".join(schema_info)
    
    def initialize_from_file(self, schema_file: str = "schema.sql"):
        """Initialize database from SQL file."""
        if not os.path.exists(schema_file):
            print(f"Schema file {schema_file} not found. Skipping initialization.")
            return
        
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(schema_sql)
            self.connection.commit()
            print(f"Database initialized from {schema_file}")
        except psycopg2.Error as e:
            self.connection.rollback()
            raise Exception(f"Schema initialization error: {str(e)}")
