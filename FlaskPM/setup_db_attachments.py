
import os

def print_setup_instructions():
    print("\n" + "="*60)
    print("ACTION REQUIRED: SETUP ATTACHMENTS")
    print("="*60)
    print("To enable File Attachments, you must perform the following actions in your Supabase Dashboard:")
    print("\n1. Run this SQL in the SQL Editor:")
    print("-" * 30)
    
    with open("setup_attachments.sql", "r") as f:
        print(f.read())
        
    print("-" * 30)
    print("\n2. Create a Storage Bucket:")
    print("   - Go to 'Storage' -> 'New Bucket'")
    print("   - Name it: 'task-attachments'")
    print("   - Set it to 'Public'")
    print("   - Save.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    print_setup_instructions()
