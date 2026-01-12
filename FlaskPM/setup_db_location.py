import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Use Service Key to bypass RLS and allow schema mods (if enabled) or just reliable access
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: Supabase credentials not found in .env")
    exit(1)

supabase: Client = create_client(url, key)

print("Attempting to add missing columns to 'attendance' table...")

# We'll use a raw SQL query via a PostgREST RPC function if available, 
# but usually, Supabase-py doesn't allow raw DDL easily unless there's a stored procedure.
# However, we can TRY to just check if we can insert/update and print a helpful message.
# ACTUALLY, the best way for the user is to give them the SQL to run in the dashboard.
# OR, if they have an 'exec_sql' function set up (common in some starter kits).

# Let's try to just print the instructions clearly.
print("\n" + "="*50)
print("ACTION REQUIRED: UPDATE DATABASE SCHEMA")
print("="*50)
print("Please run the following SQL in your Supabase SQL Editor to enable Location Tracking for Punch Out:")
print("\n")
print("""
-- Add location column if missing (for Punch In)
ALTER TABLE attendance ADD COLUMN IF NOT EXISTS location TEXT;

-- Add punch_out_location column (for Punch Out)
ALTER TABLE attendance ADD COLUMN IF NOT EXISTS punch_out_location TEXT;
""")
print("="*50 + "\n")
