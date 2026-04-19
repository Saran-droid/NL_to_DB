"""Main application for natural language to SQL query system."""
from nl_to_sql import NLToSQL
from database import Database
import json


def print_results(results, query):
    """Pretty print query results."""
    print("\n" + "="*80)
    print("GENERATED SQL QUERY:")
    print("-"*80)
    print(query)
    print("="*80)
    
    if not results:
        print("\nNo results found.")
        return
    
    print(f"\nRESULTS ({len(results)} rows):")
    print("-"*80)
    
    # Print as formatted JSON
    for i, row in enumerate(results, 1):
        print(f"\nRow {i}:")
        print(json.dumps(row, indent=2, default=str))
    
    print("="*80)


def main():
    """Run the NL to SQL application."""
    print("Natural Language to SQL Query System")
    print("Using Groq's llama-3.3-70b-versatile model")
    print("="*80)
    
    # Initialize database
    db = Database()
    db.connect()
    
    # Check if database needs initialization
    try:
        db.get_schema()
    except:
        print("\nInitializing database from schema.sql...")
        db.initialize_from_file()
    
    # Get schema
    schema = db.get_schema()
    print("\nDatabase Schema:")
    print(schema)
    print("\n" + "="*80)
    
    # Initialize NL to SQL converter
    try:
        nl_to_sql = NLToSQL()
        nl_to_sql.set_schema(schema)
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nPlease create a .env file with your GROQ_API_KEY")
        print("You can copy .env.example and add your API key")
        return
    
    print("\nReady! Enter your questions in natural language.")
    print("Type 'exit' or 'quit' to stop.\n")
    
    # Interactive loop
    while True:
        try:
            user_input = input("\nYour question: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            # Generate SQL query
            print("\nGenerating SQL query...")
            result = nl_to_sql.generate_with_explanation(user_input)
            
            sql_query = result['query']
            explanation = result['explanation']
            
            print(f"\nExplanation: {explanation}")
            
            # Execute query
            print("\nExecuting query...")
            results = db.execute_query(sql_query)
            
            # Print results
            print_results(results, sql_query)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again with a different question.")
    
    # Cleanup
    db.close()


if __name__ == "__main__":
    main()
