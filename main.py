from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional, Union
from pydantic import BaseModel
import requests
import os
from data_manager import DataManager

# Inicializar FastAPI
app = FastAPI(
    title="API de Información sobre Víctimas",
    description="API para consultar y registrar información sobre fallecidos y rescatados en la tragedia de Jet Set",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de API Key
API_KEY = "1901"
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Inicializar gestor de datos
data_manager = DataManager()

# Azure OpenAI Configuration
AZURE_API_KEY = os.getenv("AZURE_API_KEY",
                          "DZKAe2jMOWbZJlqrBurzm0p2wU4lAoJ7BvAb97jlXZWXu3q5iCEfJQQJ99BDACHYHv6XJ3w3AAABACOGBq1S")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "https://rag-codec-v1.openai.azure.com/")
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT", "gpt-4o-mini-codec")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")


# Modelos de datos
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class FallecidoRequest(BaseModel):
    nombre: str


class PacienteRequest(BaseModel):
    nombre: str
    hospital: str
    edad: Optional[int] = None


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict] = None


# Middleware para validar API Key
async def get_api_key(api_key: str = Header(None, alias=API_KEY_NAME)):
    if api_key is None or api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida o faltante"
        )
    return api_key


# Función para generar respuesta de Azure OpenAI
def generate_azure_response(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY
    }

    # Obtener todos los datos de víctimas formateados
    data_text = data_manager.get_data_for_model()

    # Construir el mensaje del sistema con los datos y las instrucciones
    system_message = (
        "Eres un asistente que proporciona información sobre la tragedia de la discoteca Jet Set en República Dominicana. "
        "Analiza cuidadosamente la siguiente información actualizada sobre las víctimas:\n\n"
        f"{data_text}\n\n"
        "Cuando te pregunten por una persona específica:\n"
        "1. Busca exactamente si esa persona aparece en la lista de fallecidos o de pacientes en hospitales.\n"
        "2. Si la persona está en la lista de fallecidos, expresa tus condolencias.\n"
        "3. Si la persona está en un hospital, indica el hospital y su edad si está disponible.\n"
        "4. Si la persona no aparece en ninguna lista, indica claramente que no tienes información sobre esa persona.\n"
        "5. Responde con empatía y precisión, esta información es muy sensible."
    )

    payload = {
        "messages": [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "stream": False
    }

    url = f"{AZURE_ENDPOINT}/openai/deployments/{AZURE_DEPLOYMENT}/chat/completions?api-version={AZURE_API_VERSION}"

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
        else:
            return f"Error al obtener respuesta: {response.status_code}"
    except Exception as e:
        return f"Error al conectar con Azure OpenAI: {str(e)}"


# Endpoints
@app.get("/", dependencies=[Depends(get_api_key)])
async def root():
    return {"message": "API de Información sobre Víctimas activa"}


@app.post("/chat", response_model=ChatResponse, dependencies=[Depends(get_api_key)])
async def chat(request: ChatRequest):
    # Enviar la consulta directamente a Azure OpenAI con todos los datos
    response = generate_azure_response(request.message)
    return ChatResponse(response=response)


@app.post("/fallecidos/registrar", response_model=ApiResponse, dependencies=[Depends(get_api_key)])
async def registrar_fallecido(request: FallecidoRequest):
    if not request.nombre or request.nombre.strip() == "":
        return ApiResponse(success=False, message="El nombre no puede estar vacío")

    result = data_manager.add_fallecido(request.nombre)
    if result:
        return ApiResponse(success=True, message=f"{request.nombre} ha sido registrado como fallecido")
    else:
        return ApiResponse(success=False, message=f"{request.nombre} ya está registrado como fallecido")


@app.post("/pacientes/registrar", response_model=ApiResponse, dependencies=[Depends(get_api_key)])
async def registrar_paciente(request: PacienteRequest):
    if not request.nombre or request.nombre.strip() == "":
        return ApiResponse(success=False, message="El nombre no puede estar vacío")

    if not request.hospital or request.hospital.strip() == "":
        return ApiResponse(success=False, message="El hospital no puede estar vacío")

    result = data_manager.add_paciente(request.nombre, request.hospital, request.edad)
    if result["success"]:
        return ApiResponse(success=True,
                           message=f"{request.nombre} ha sido registrado como paciente en {request.hospital}")
    else:
        return ApiResponse(success=False, message=result["message"])


@app.get("/datos", dependencies=[Depends(get_api_key)])
async def obtener_datos():
    return data_manager.get_all_data()


# Manejo de errores
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": f"Error interno: {str(exc)}"},
    )


# Punto de entrada
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)