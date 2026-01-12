from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# 1. Corregimos las importaciones
from src.api.routes.inventory import router as equipment_router
# Asumiendo que en src/api/routes/persons.py definiste 'router'
from src.api.routes.persons import router as person_router 
from src.api.errors import global_exception_handler

load_dotenv()

app = FastAPI(
    title="Inventory API - Clean Architecture",
    description="Sistema de gestión de inventarios con FastAPI y Supabase",
    version="1.0.0"
)

# Configuración de Errores Globales
app.add_exception_handler(Exception, global_exception_handler)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # O ["*"] para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Registro de rutas con prefijos claros
# Es recomendable usar prefijos para mantener el orden
app.include_router(equipment_router, prefix="/api", tags=["Equipments"])
app.include_router(person_router, prefix="/api", tags=["personas"])

@app.get("/")
def read_root():
    return {"message": "Inventory API Running"}

@app.get("/health")
def health_check():
    return {"status": "online", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    # Importante: El string "src.main:app" debe coincidir con la ruta de tu archivo
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)