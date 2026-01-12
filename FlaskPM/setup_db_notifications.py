import os
from supabase import create_client

# Define Supabase credentials manually or load from env
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_SERVICE_KEY not found in environment.")
    print("Please make sure you have set these variables.")
    # Fallback to loading from .env file if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
    except ImportError:
        pass

if not url or not key:
    print("CRITICAL: Cannot connect to Supabase without URL and Service Key.")
    exit(1)

supabase = create_client(url, key)

print("Connected to Supabase. Attempting to update 'tasks' table...")

# SQL to run
# Note: Supabase-py doesn't support executing raw SQL easily on the client side 
# unless we use the rpc call or if we assume the user can run SQL in dashboard.
# However, we can use the PostgreSQL function approach if we had one.
# But since we are likely allowed to run SQL in the dashboard, I will print instructions.
# OR providing a python script that uses `postgres` library if installed? No.

# Wait, the user asked me to "do" it. I can't execute DDL via standard Supabase client 
# unless I have a stored procedure for it.
# BUT, I can try to see if the columns exist by fetching a record.

try:
    # Instructions for User
    print("\n" + "="*50)
    print("IMPORTANT: DATABASE UPDATE REQUIRED")
    print("="*50)
    print("To support deadline notifications, please run the following SQL in your Supabase SQL Editor:\n")
    
    print("""
    ALTER TABLE tasks 
    ADD COLUMN IF NOT EXISTS reminder_sent BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS overdue_notified BOOLEAN DEFAULT FALSE;
    """)
    
    print("\n" + "="*50)
    
except Exception as e:
    print(f"Error: {e}")
