"""Streamlit frontend for Natural Language to SQL system."""
import streamlit as st
import requests
import pandas as pd
import json
from typing import Dict, Any, List


# Configuration
API_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Natural Language to SQL",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sql-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .example-button {
        margin: 0.2rem 0;
    }
</style>
""", unsafe_allow_html=True)


def check_api_health() -> Dict[str, Any]:
    """Check if the API is running and healthy."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.json()
    except requests.exceptions.RequestException:
        return {"status": "offline", "database_connected": False, "groq_configured": False}


def get_schema() -> Dict[str, Any]:
    """Get database schema from API."""
    try:
        response = requests.get(f"{API_URL}/schema", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching schema: {str(e)}")
        return None


def get_examples() -> List[Dict[str, Any]]:
    """Get example questions from API."""
    try:
        response = requests.get(f"{API_URL}/examples", timeout=5)
        response.raise_for_status()
        return response.json()["examples"]
    except requests.exceptions.RequestException:
        return []


def execute_query(question: str, explain: bool = True) -> Dict[str, Any]:
    """Execute a natural language query via API."""
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={"question": question, "explain": explain},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"API request failed: {str(e)}",
            "question": question,
            "sql_query": "",
            "results": [],
            "row_count": 0
        }


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<div class="main-header">🤖 Natural Language to SQL</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ask questions in plain English, get SQL queries and results</div>', unsafe_allow_html=True)
    
    # Check API health
    health = check_api_health()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ System Status")
        
        if health["status"] == "offline":
            st.error("🔴 API Offline")
            st.warning("Please start the backend server:\n```bash\ncd backend\nuvicorn api:app --reload\n```")
            st.stop()
        elif health["status"] == "healthy":
            st.success("🟢 API Online")
            st.success("🟢 Database Connected")
            st.success("🟢 Groq Configured")
        else:
            st.warning("🟡 API Degraded")
            if not health["database_connected"]:
                st.error("🔴 Database Disconnected")
            if not health["groq_configured"]:
                st.error("🔴 Groq Not Configured")
        
        st.divider()
        
        # Database Schema
        st.header("📊 Database Schema")
        if st.button("🔄 Refresh Schema"):
            st.rerun()
        
        schema_data = get_schema()
        if schema_data:
            st.subheader("Tables")
            for table in schema_data["tables"]:
                st.markdown(f"- **{table}**")
            
            with st.expander("View Full Schema"):
                st.code(schema_data["schema"], language="sql")
        
        st.divider()
        
        # Example Questions
        st.header("💡 Example Questions")
        examples = get_examples()
        
        for category_data in examples:
            with st.expander(category_data["category"]):
                for question in category_data["questions"]:
                    if st.button(question, key=f"example_{question}", use_container_width=True):
                        st.session_state.selected_question = question
                        st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔍 Ask Your Question")
        
        # Get question from session state if example was clicked
        default_question = st.session_state.get("selected_question", "")
        
        # Question input
        question = st.text_area(
            "Enter your question in natural language:",
            value=default_question,
            height=100,
            placeholder="e.g., Show me all users older than 30",
            help="Ask any question about your database in plain English"
        )
        
        # Clear selected question after using it
        if "selected_question" in st.session_state:
            del st.session_state.selected_question
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            execute_btn = st.button("🚀 Execute Query", type="primary", use_container_width=True)
        
        with col_btn2:
            clear_btn = st.button("🗑️ Clear", use_container_width=True)
        
        if clear_btn:
            st.rerun()
    
    with col2:
        st.header("⚡ Quick Actions")
        st.info("💡 Click on example questions in the sidebar to try them out!")
        
        # Query history
        if "query_history" not in st.session_state:
            st.session_state.query_history = []
        
        if st.session_state.query_history:
            st.subheader("📜 Recent Queries")
            for i, hist_q in enumerate(reversed(st.session_state.query_history[-5:])):
                if st.button(f"🔄 {hist_q[:40]}...", key=f"history_{i}", use_container_width=True):
                    st.session_state.selected_question = hist_q
                    st.rerun()
    
    # Execute query
    if execute_btn and question.strip():
        with st.spinner("🔄 Processing your question..."):
            result = execute_query(question, explain=True)
        
        # Add to history
        if question not in st.session_state.query_history:
            st.session_state.query_history.append(question)
        
        st.divider()
        
        if result["success"]:
            # Success message
            st.markdown(f'<div class="success-box">✅ Query executed successfully! Found {result["row_count"]} rows.</div>', unsafe_allow_html=True)
            
            # Show explanation if available
            if result.get("explanation"):
                with st.expander("💡 Explanation", expanded=True):
                    st.info(result["explanation"])
            
            # Show SQL query
            st.subheader("📝 Generated SQL Query")
            st.code(result["sql_query"], language="sql")
            
            # Copy button for SQL
            if st.button("📋 Copy SQL to Clipboard"):
                st.code(result["sql_query"], language="sql")
                st.success("SQL copied! (Use Ctrl+C to copy from the code block above)")
            
            # Show results
            st.subheader("📊 Query Results")
            
            if result["results"]:
                # Convert to DataFrame for better display
                df = pd.DataFrame(result["results"])
                
                # Display as table
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Download options
                col_d1, col_d2, col_d3 = st.columns(3)
                
                with col_d1:
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col_d2:
                    json_str = df.to_json(orient="records", indent=2)
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_str,
                        file_name="query_results.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col_d3:
                    # Show statistics
                    with st.expander("📈 Statistics"):
                        st.write(f"**Total Rows:** {len(df)}")
                        st.write(f"**Total Columns:** {len(df.columns)}")
                        st.write(f"**Columns:** {', '.join(df.columns)}")
                
            else:
                st.info("No results found for this query.")
        
        else:
            # Error message
            st.markdown(f'<div class="error-box">❌ Error: {result["error"]}</div>', unsafe_allow_html=True)
            
            if result.get("sql_query"):
                st.subheader("Generated SQL (with error)")
                st.code(result["sql_query"], language="sql")
    
    elif execute_btn:
        st.warning("⚠️ Please enter a question first!")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Powered by <strong>Groq</strong> (llama-3.3-70b-versatile) and <strong>PostgreSQL</strong></p>
        <p>💡 Tip: Be specific in your questions for better results</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
