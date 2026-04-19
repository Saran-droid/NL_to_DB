"""Natural Language to SQL Query System.

A Python package that converts natural language questions into SQL queries
using Groq's LLM and executes them against PostgreSQL databases.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

from .converter import NLToSQL
from .database import Database

__all__ = ["NLToSQL", "Database"]
