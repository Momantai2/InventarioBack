import jwt
import json
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Esquema para extraer el token del header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Obtenemos la llave pública (JWK) de Supabase desde el entorno
    jwk_env = os.getenv("SUPABASE_JWK")
    
    if not jwk_env:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Configuración JWK de autenticación faltante en el servidor"
        )

    try:
        # Convertimos el string JSON del .env a diccionario
        jwk_dict = json.loads(jwk_env)
        
        # Obtenemos la llave de firma (Supabase usa ES256 comúnmente)
        signing_key = jwt.PyJWK(jwk_dict)
        
        # Decodificamos y validamos el token
        payload = jwt.decode(
            token, 
            signing_key.key, 
            algorithms=["ES256"], 
            options={"verify_aud": False} # Supabase a veces requiere esto dependiendo de la config
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="El token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Error de autenticación: {str(e)}")