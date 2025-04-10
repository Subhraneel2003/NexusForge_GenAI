# Import this at the very beginning of your app.py
import sys
import importlib.util

def fix_sqlite():
    try:
        import pysqlite3
        sys.modules['sqlite3'] = pysqlite3
        print("SQLite version successfully patched for ChromaDB")
    except ImportError:
        print("Couldn't patch SQLite - add pysqlite3-binary to requirements.txt")
