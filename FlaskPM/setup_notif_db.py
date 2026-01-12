from utils import supabase

print("Adding 'is_read' column to notifications table...")
try:
    # Just run a check, user might need to run SQL manually if clientside execution fails for DDL
    print("""
    Please run the following SQL in Supabase Dashboard:
    
    ALTER TABLE notifications 
    ADD COLUMN IF NOT EXISTS is_read BOOLEAN DEFAULT FALSE;
    """)
    
    # Try to verify if it exists
    res = supabase.table("notifications").select("is_read").limit(1).execute()
    print("Column 'is_read' already exists.")
except Exception as e:
    print(f"Verification failed (Column likely missing): {e}")
