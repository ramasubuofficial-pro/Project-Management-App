from supabase import create_client, Client
from config import Config

def get_supabase() -> Client:
    url = Config.SUPABASE_URL
    key = Config.SUPABASE_KEY
    if not url or not key:
        return None
    return create_client(url, key)

supabase = get_supabase()

def get_supabase_admin() -> Client:
    url = Config.SUPABASE_URL
    key = Config.SUPABASE_SERVICE_KEY
    if not url or not key:
        return None
    return create_client(url, key)
