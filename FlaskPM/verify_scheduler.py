from utils import supabase
from datetime import datetime

try:
    print("--- CHECKING NOTIFICATIONS ---")
    # Fetch last 5 notifications
    res = supabase.table("notifications").select("*").order("created_at", desc=True).limit(5).execute()
    notifs = res.data
    
    if not notifs:
        print("No notifications found.")
    else:
        for n in notifs:
            print(f"[{n['created_at']}] To User {n['user_id']}: {n['title']} - {n['message']}")

    print("\n--- CHECKING TARGET TASK ---")
    # Try to find the task due on Jan 12, 2026 at 11:45 PM
    # 2026-01-12 23:45
    # We'll just list active tasks for simplicity
    res = supabase.table("tasks").select("*").neq("status", "Completed").execute()
    tasks = res.data
    
    found = False
    for t in tasks:
        d = t.get('deadline')
        print(f"Task: {t.get('title')} | Deadline: {d}")
        if d and '2026-01-12' in d: # Simple match
             found = True
             # Check if we can read the extra columns
             reminded = t.get('reminder_sent', 'COLUMN_MISSING')
             print(f"   -> Reminder Sent Status: {reminded}")

except Exception as e:
    print(f"Error: {e}")
