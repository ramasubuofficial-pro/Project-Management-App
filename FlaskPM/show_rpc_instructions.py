
def print_instructions():
    print("\n" + "*"*60)
    print("FINAL SOLUTION: SECURE FUNCTION")
    print("*"*60)
    print("\nWe will bypass the security checks using a Database Function.")
    print("This is the standard way to handle complex permission issues in Supabase.")
    print("\nPLEASE FOLLOW THESE STEPS:")
    print("1. Open your Supabase Dashboard: https://supabase.com/dashboard/project/_/sql")
    print("2. Click 'New Query'")
    print("3. Copy and Run this SQL:")
    print("\n" + "-"*40)
    
    with open("setup_rpc.sql", "r") as f:
        print(f.read())
        
    print("-" * 40)
    print("*"*60 + "\n")

if __name__ == "__main__":
    print_instructions()
