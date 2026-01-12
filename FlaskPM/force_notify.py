from utils import supabase, get_supabase_admin
from config import Config

admin = get_supabase_admin()

print("Forcing check for latest task...")

# Get latest task
res = admin.table("tasks").select("*").order("created_at", desc=True).limit(1).execute()
if res.data:
    task = res.data[0]
    print(f"Checking Task: {task['title']}")
    
    # Send Notification immediately
    user_id = task.get('assigned_to')
    if user_id:
        print(f"Sending notification to {user_id}...")
        admin.table("notifications").insert({
            "user_id": user_id,
            "title": "Deadline Reminder (Test)",
            "message": f"Reminder: Task '{task['title']}' is due soon!",
            "link": f"/projects/{task['project_id']}"
        }).execute()
        print("Notification sent!")
    else:
        print("No assignee.")
else:
    print("No tasks found.")
