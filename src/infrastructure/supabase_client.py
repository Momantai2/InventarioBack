import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY") # service_role key
    
    if not url or not key:
        raise ValueError("Faltan las credenciales de Supabase en el archivo .env")
        
    return create_client(url, key)

# Instancia única para reutilizar
supabase: Client = get_supabase_client()