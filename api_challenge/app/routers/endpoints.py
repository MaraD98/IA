from fastapi import APIRouter, HTTPException, status
from app.models.schemas import InputUpLoad, InputEmbeddings, InputSearch, InputAsk, OutUp, OutEmbeddings, OutSearch, OutAsk
import chromadb
import uuid
from typing import List,Dict, Any
from pydantic import BaseModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.utils.utils import split_text, get_embeddings

# Inicialización del cliente los clientes
router = APIRouter()
#co = cohere.ClientV2()
chroma_client = chromadb.Client() 
documents = chroma_client.create_collection(name="Documentos")

#POST /upload
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


#POST /generate-embeddings

@router.post("/generate-ebeddings", response_model=OutEmbeddings, status_code= status.HTTP_201_CREATED, description="Carga ebeddings y lo almacena en ChromaDB.")
async def insertEbeddings(input_embe: InputEmbeddings):
    try:
        print(f"recibo id {input_embe.document_id}")
        docs = documents.get(ids=[input_embe.document_id], include=["documents", "metadatas"])  
        print(f"guardo el doc {docs}")

        if not docs["documents"]:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado o sin contenido.")

        document_content = docs["documents"][0]
        print(f"existe y este es su contenido {document_content}")

        # Divide el texto en chunks
        chunks = split_text(document_content)

        # Genera embeddings
        cohere_embeddings =  get_embeddings(chunks)


        # Añade los embeddings a la base

        for chunk, embedding in zip(chunks, cohere_embeddings):
            documents.add(
                ids=[input_embe.document_id],  # Usar el mismo ID para cada chunk
                embeddings=[embedding],
                documents=[chunk]
            )


        return {"message": f"Embeddings cargados con éxito, para el documento {input_embe.document_id}"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f"Error al generar embeddings: {str(e)}")      










#pruebas

#  modelo de salida para los documentos
class DocumentResponse(BaseModel):
    ids: List[str]
    documents: List[str]
    metadatas: List[Dict[str, str]]


#pruebas


@router.get("/validar-documentos", response_model=List[Dict[str, Any]])
async def validar_documentos():
    try:
        # Obt de documentos y metadatos
        docs = documents.get(include=["documents", "metadatas"])  
        # documentos y metadatos en un formato adecuado
        resultado = [
            {"documento": doc, "metadata": meta}
            for doc, meta in zip(docs["documents"], docs["metadatas"])
        ]
        return resultado
    except Exception as e:
        return {"detail": f"Error al obtener los documentos: {str(e)}"}



