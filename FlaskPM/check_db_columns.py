from utils import supabase

try:
    print("Checking 'tasks' table for 'reminder_sent' column...")
    # Try to select the specific column. If it doesn't exist, this should fail.
    res = supabase.table("tasks").select("reminder_sent").limit(1).execute()
    print("SUCCESS: Column 'reminder_sent' exists.")
except Exception as e:
    print(f"FAILURE: {e}")

try:
    print("Checking 'tasks' table for 'overdue_notified' column...")
    res = supabase.table("tasks").select("overdue_notified").limit(1).execute()
    print("SUCCESS: Column 'overdue_notified' exists.")
except Exception as e:
    print(f"FAILURE: {e}")
