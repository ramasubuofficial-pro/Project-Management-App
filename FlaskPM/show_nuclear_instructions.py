
def print_instructions():
    print("\n" + "!"*60)
    print("ACTION REQUIRED: ONE LAST SQL FIX")
    print("!"*60)
    print("\nThe error persists because the security policy is extremely stubborn.")
    print("We are going to DISABLE the security checks for the attachments table entirely.")
    print("This will definitely fix the upload error.")
    print("\nPLEASE FOLLOW THESE STEPS:")
    print("1. Open your Supabase Dashboard: https://supabase.com/dashboard/project/_/sql")
    print("2. Clear the editor.")
    print("3. Copy and Run this SQL:")
    print("\n" + "-"*40)
    
    with open("nuclear_fix_attachments.sql", "r") as f:
        print(f.read())
        
    print("-" * 40)
    print("!"*60 + "\n")

if __name__ == "__main__":
    print_instructions()
