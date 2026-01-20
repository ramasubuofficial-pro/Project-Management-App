
def print_instructions():
    print("\n" + "!"*60)
    print("ACTION REQUIRED: RUN UPDATED SQL")
    print("!"*60)
    print("\nThe previous error occurred because the policy already existed.")
    print("I have updated the script to handle this case.")
    print("\nPLEASE FOLLOW THESE STEPS:")
    print("1. Open your Supabase Dashboard: https://supabase.com/dashboard/project/_/sql")
    print("2. Clear the previous query.")
    print("3. Copy and Run the NEW SQL code below:")
    print("\n" + "-"*40)
    
    with open("final_db_fix_v2.sql", "r") as f:
        print(f.read())
        
    print("-" * 40)
    print("!"*60 + "\n")

if __name__ == "__main__":
    print_instructions()
