
import os
from dotenv import load_dotenv

load_dotenv()

def check_env():
    print("\n" + "="*40)
    print("ENVIRONMENT DEBUG CHECK")
    print("="*40)
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    service_key = os.getenv('SUPABASE_SERVICE_KEY')
    
    print(f"SUPABASE_URL:         {'FOUND' if url else 'MISSING'}")
    print(f"SUPABASE_KEY:         {'FOUND' if key else 'MISSING'}")
    print(f"SUPABASE_SERVICE_KEY: {'FOUND' if service_key else 'MISSING'}")
    
    if service_key:
        print(f"Service Key Start:    {service_key[:10]}...")
    else:
        print("CRITICAL: SUPABASE_SERVICE_KEY is missing. This forces the app to use the restricted Anon key.")

    print("\n" + "="*40)

if __name__ == "__main__":
    check_env()
