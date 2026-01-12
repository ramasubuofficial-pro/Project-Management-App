import requests
import json
from flask import session

# We can't easily use 'requests' with the Flask session cookie unless we login first.
# Instead, let's use the verify_scheduler.py approach but printing validation.

from utils import supabase

print("--- INSPECTING NOTIFICATIONS DATA ---")
try:
    # Mimic the query in api_routes
    # res = supabase.table("notifications").select("*").eq("user_id", user_id)...
    # We'll just fetch *all* to see structure.
    res = supabase.table("notifications").select("*").order("created_at", desc=True).limit(5).execute()
    data = res.data
    
    print(f"Fetched {len(data)} rows.")
    for i, n in enumerate(data):
        print(f"[{i}] ID: {n.get('id')} ({type(n.get('id'))})")
        print(f"    Title: {n.get('title')}")
        print(f"    Link: {n.get('link')}")
        print(f"    IsRead: {n.get('is_read')} ({type(n.get('is_read'))})")
        print(f"    CreatedAt: {n.get('created_at')}")
        
        # Check for potential JS breaking chars
        link = n.get('link')
        if link and "'" in link:
            print("    [WARNING] Link contains single quote!")

    # Check unread count query
    # unread_res = supabase.table("notifications").select("id", count='exact').eq("is_read", False).execute()
    # print(f"Unread Count: {unread_res.count}")

except Exception as e:
    print(f"Error: {e}")
