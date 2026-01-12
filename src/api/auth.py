import jwt
import json
from jwt import PyJWKClient # Nueva importación
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pega aquí el JSON que te dio Supabase entre las comillas triples


def get_current_user(token: str = Depends(oauth2_scheme)):
    # Obtenemos el texto del .env
    jwk_env = os.getenv("SUPABASE_JWK")
    
    if not jwk_env:
        raise HTTPException(status_code=500, detail="Configuración JWK faltante")

    try:
        # Convertimos el texto a diccionario de Python
        jwk_dict = json.loads(jwk_env)
        
        # Obtenemos la llave para validar
        signing_key = jwt.PyJWK(jwk_dict)
        
        payload = jwt.decode(
            token, 
            signing_key.key, 
            algorithms=["ES256"], 
            options={"verify_aud": False}
        )
        return payload
    except Exception as e:
        print(f"Error Auth: {e}")
        raise HTTPException(status_code=401, detail="No autorizado")