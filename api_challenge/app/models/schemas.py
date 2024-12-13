from pydantic import BaseModel, Field
from typing import List

#Estructura de datos INPUT

class InputUpLoad(BaseModel):
    title: str = Field(..., min_length=1, description="Titulo del documento(obligatorio)")
    content: str = Field(..., min_length=1, description="Contenido del documento (obligatorio)")

class InputEmbeddings(BaseModel):
    document_id: str = Field(..., pattern="^[a-zA-Z0-9_-]+$", description="ID único del documento (alfanumérico)")

class InputSearch(BaseModel):
    query: str = Field(..., min_length=1, description="Consulta en lenguaje natural (obligatorio)")

class InputAsk(BaseModel):
    question: str = Field(..., min_length=1, description="Pregunta en lenguaje natural (obligatorio)")


#Estructura de datos OUTPUT

class OutUp(BaseModel):
    message: str
    document_id: str = Field(..., pattern="^[a-zA-Z0-9_-]+$", description="ID único del documento (alfanumérico)")

class OutEmbeddings(BaseModel):
    message: str 
    document_id: int = Field(..., pattern="^[a-zA-Z0-9_-]+$", description="ID único del embedding (alfanumérico)")

class DocumentResult(BaseModel):
    document_id: str = Field(..., pattern="^[a-zA-Z0-9_-]+$", description="ID único del documento relevante (alfanumérico)")
    title: str = Field(..., max_length=255, description="Título del documento relevante (máx. 255 caracteres)")
    content_snippet: str = Field(..., description="Fragmento del contenido relevante del documento")
    similarity_score: float = Field(..., ge=0, le=1, description="Puntuación de relevancia (0 a 1)")

class OutSearch(BaseModel):
    result: List[DocumentResult] = Field(..., description="Lista de documentos relevantes para la consulta") 


#Para pruebas mas adelante
results: list[DocumentResult] = [
    {
        "document_id": "abc123",
        "title": "Título del documento",
        "content_snippet": "Fragmento relevante...",
        "similarity_score": 0.85
    }
]

class OutAsk(BaseModel):
    question: str = Field(..., min_length=1, description="Pregunta formulada por el usuario (obligatorio)")
    answer: str = Field(..., min_length=1, description="Respuesta generada basada en los documentos relevantes")

