from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()


#Validacion de datos 
class SubTarea(BaseModel):
    id: int
    title: str
    completed: bool

class Tarea(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False
    priority: Optional[int] = Field(None, ge=1, le=5)
    due_date: Optional[datetime] = None
    category: Optional[str] = None
    subtasks: List[SubTarea]

#Mi db xD
tareas=[]

#Trae la lista completa de tareas
@app.get("/tareas", response_model=List[Tarea])
async def mostrar_todos():
    return tareas

#Trae los detalles de una tarea específica por ID
@app.get("/tareas/{id}", response_model=Tarea)
async def mostrar_tarea(tarea_id: int):
    tarea = next((tarea for tarea in tareas if tarea.id == tarea_id), None)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

#Crea una nueva tarea con todos los campos requeridos
@app.post("/tareas", response_model=Tarea)
async def insertar_tarea(tarea: Tarea):
    tareas.append(tarea)
    return {"message": f"Tarea insertada: {tarea}"}

#Actualizar una tarea existente por ID 
@app.put("/tareas/{id}", response_model=Tarea)
async def actualizar_tarea(tarea_id: int, actualizare_tarea: Tarea):
    tarea = next((tarea for tarea in tareas if tarea.id == tarea_id), None)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Actualiza los campos de la tarea
    tarea.title = actualizare_tarea.title
    tarea.description = actualizare_tarea.description
    tarea.completed = actualizare_tarea.completed
    tarea.priority = actualizare_tarea.priority
    tarea.due_date = actualizare_tarea.due_date
    tarea.subtasks = actualizare_tarea.subtasks
    
    return tarea

#Eliminar una tarea por su ID
@app.delete("/tareas/{id}", response_model=Tarea)
async def eliminar_tarea(id: int):
    tarea = next((tarea for tarea in tareas if tarea.id == id), None)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tareas.remove(tarea)
    return tarea



