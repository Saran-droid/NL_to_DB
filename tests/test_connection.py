"""Test PostgreSQL connection and setup."""
from nl_to_sql.database import Database
import os
from dotenv import load_dotenv


def test_connection():
    """Test basic PostgreSQL connection."""
    load_dotenv()
    
    print("="*80)
    print("PostgreSQL Connection Test")
    print("="*80)
    
    # Show configuration (without password)
    print("\nConfiguration:")
    print(f"  Host: {os.getenv('POSTGRES_HOST', 'localhost')}")
    print(f"  Port: {os.getenv('POSTGRES_PORT', '5432')}")
    print(f"  Database: {os.getenv('POSTGRES_DB', 'nl_to_sql_db')}")
    print(f"  User: {os.getenv('POSTGRES_USER', 'postgres')}")
    print(f"  Password: {'*' * len(os.getenv('POSTGRES_PASSWORD', ''))}")
    
    try:
        print("\nConnecting to PostgreSQL...")
        db = Database()
        db.connect()
        print("✓ Connection successful!")
        
        # Test query
        print("\nTesting query execution...")
        result = db.execute_query("SELECT version()")
        print(f"✓ PostgreSQL version: {result[0]['version'][:50]}...")
        
        # Check if tables exist
        print("\nChecking for existing tables...")
        tables = db.execute_query("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        if tables:
            print(f"✓ Found {len(tables)} existing tables:")
            for table in tables:
                print(f"  - {table['table_name']}")
        else:
            print("  No tables found. Will initialize from schema.sql")
            
            # Initialize database
            print("\nInitializing database from schema.sql...")
            db.initialize_from_file()
            
            # Verify initialization
            print("\nVerifying initialization...")
            users = db.execute_query("SELECT COUNT(*) as count FROM users")
            products = db.execute_query("SELECT COUNT(*) as count FROM products")
            orders = db.execute_query("SELECT COUNT(*) as count FROM orders")
            
            print(f"✓ Users: {users[0]['count']} rows")
            print(f"✓ Products: {products[0]['count']} rows")
            print(f"✓ Orders: {orders[0]['count']} rows")
        
        # Get and display schema
        print("\n" + "="*80)
        print("Database Schema:")
        print("="*80)
        schema = db.get_schema()
        print(schema)
        
        # Test sample query
        print("\n" + "="*80)
        print("Sample Query Test:")
        print("="*80)
        print("\nQuery: SELECT name, email FROM users LIMIT 3")
        users = db.execute_query("SELECT name, email FROM users LIMIT 3")
        
        print(f"\nResults ({len(users)} rows):")
        for user in users:
            print(f"  - {user['name']} ({user['email']})")
        
        db.close()
        
        print("\n" + "="*80)
        print("✓ All tests passed!")
        print("="*80)
        print("\nYou're ready to use the NL to SQL system!")
        print("Run: uv run main.py")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your .env file has correct credentials")
        print("3. Verify the database exists: psql -U postgres -c 'CREATE DATABASE nl_to_sql_db;'")
        print("4. See setup_postgres.md for detailed setup instructions")
        return False
    
    return True


if __name__ == "__main__":
    test_connection()
