from fastapi import APIRouter, HTTPException, status
from app.models.schemas import InputUpLoad, InputEmbeddings, InputSearch, InputAsk, OutUp, OutEmbeddings, OutSearch, OutAsk
import chromadb
import uuid
from typing import List,Dict, Any
from pydantic import BaseModel

router = APIRouter()

# Inicialización del cliente de ChromaDB
chroma_client = chromadb.Client()
documents = chroma_client.create_collection(name="Documentos")

@router.post("/upload", response_model=OutUp, status_code= status.HTTP_201_CREATED, description="Carga un nuevo documento en el sistema y lo almacena en ChromaDB.")
async def insertDocument(input_up: InputUpLoad):
    # Generar un ID único alfanumérico para el documento
    try: 
        document_id = str(uuid.uuid4()).replace("-", "")[:5]

        documents.add(
                    ids= [document_id], 
                    metadatas=[{"title": input_up.title}], 
                    documents=[input_up.content]
                    )
        return {"message": "Documento cargado con éxito", "document_id": document_id}
    except Exception as e:
        # Manejo de error general
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f"Error al cargar el documento: {str(e)}")












#pruebas

# Definir el modelo de salida para los documentos
class DocumentResponse(BaseModel):
    ids: List[str]
    documents: List[str]
    metadatas: List[Dict[str, str]]


#pruebas


@router.get("/validar-documentos", response_model=List[Dict[str, Any]])
async def validar_documentos():
    try:
        # Obtenemos documentos y metadatos
        docs = documents.get(include=["documents", "metadatas"])  
        # Combinamos documentos y metadatos en un formato adecuado
        resultado = [
            {"documento": doc, "metadata": meta}
            for doc, meta in zip(docs["documents"], docs["metadatas"])
        ]
        return resultado
    except Exception as e:
        return {"detail": f"Error al obtener los documentos: {str(e)}"}


###cohere
#import cohere
#co = cohere.ClientV2()
