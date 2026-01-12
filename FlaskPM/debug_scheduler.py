from utils import supabase
from datetime import datetime, timezone
import math

print("--- DEBUG DIAGNOSIS ---")

try:
    # 1. Fetch all tasks
    res = supabase.table("tasks").select("*").order("created_at", desc=True).limit(5).execute()
    tasks = res.data

    print(f"Found {len(tasks)} recent tasks.")

    for t in tasks:
        title = t.get('title')
        deadline_str = t.get('deadline')
        
        print(f"\nTask: {title}")
        print(f"Deadline (DB): {deadline_str}")
        
        # Check Columns
        has_remind_col = 'reminder_sent' in t
        val_remind = t.get('reminder_sent')
        print(f"Has 'reminder_sent' column? {has_remind_col}")
        print(f"Value: {val_remind}")

        if deadline_str:
            # Parse
            # DB dates are usually ISO UTC
            deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
            
            # Current UTC
            now = datetime.now(timezone.utc)
            
            diff = deadline - now
            hours = diff.total_seconds() / 3600
            print(f"Hours Remaining: {hours:.2f}")
            
            if 0 < hours <= 12:
                print(">> CONDITION MET: < 12 hours.")
                if not has_remind_col:
                     print("!! ERROR: Cannot save reminder status (Column missing)")
                elif not val_remind:
                     print(">> ACTION: System WOULD send notification now.")
                else:
                     print(">> STATUS: Already reminded.")
            else:
                print(">> Condition NOT met (Time > 12h or Passed).")

except Exception as e:
    print(f"Error: {e}")
