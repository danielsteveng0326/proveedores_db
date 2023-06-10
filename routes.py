from fastapi import APIRouter, HTTPException
from typing import List
from db.models.schemas import ContractorCreate
from db.client import db_client
from db.models.schemas import ContractorCreate
from bson import json_util


contractors_router = APIRouter()



@contractors_router.get("/")
async def get_home():
    return {"message":"Bienvenido a la API de contratos y contratistas"}

@contractors_router.post("/contractor", response_model=ContractorCreate)
async def create_contractor(contractor: ContractorCreate):
        existing_contractor = db_client.local.contratistas.find_one({"contractor_id": contractor.contractor_id})
        if existing_contractor:
                raise HTTPException(status_code=400, detail="El contratista ya existe")
    
    # Realizar las validaciones adicionales aquí antes de guardar el contratista
        if contractor.tipo_id == "Cédula" and contractor.contractor_id < 100000:
            raise HTTPException(status_code=400, detail="Número de ID inválido para Cédula")
        if contractor.tipo_id == "NIT" and contractor.contractor_id < 99999999 :
            raise HTTPException(status_code=400, detail="Número de ID inválido para NIT")
        if contractor.tipo_id_rep_legal == "Cédula" and contractor.numero_id_rep_legal < 100000:
            raise HTTPException(status_code=400, detail="Número de ID del Representante Legal inválido para Cédula")
        if contractor.tipo_id_rep_legal == "NIT" and contractor.numero_id_rep_legal != 9:
            raise HTTPException(status_code=400, detail="Número de ID del Representante Legal inválido para NIT")
        
        contr_dict = dict(contractor)
        
        db_client.local.contratistas.insert_one(contr_dict)

        return contractor

@contractors_router.get("/contractor/{contractor_id}", response_model=ContractorCreate)
async def get_contractor(contractor_id: int):
    contractor = db_client.local.contratistas.find_one({"contractor_id": contractor_id})
    if not contractor:
        raise HTTPException(status_code=404, detail="Contratista no encontrado")
    return contractor


@contractors_router.get("/contractors", response_model=List[ContractorCreate])
async def get_contractors():
    contractors = list(db_client.local.contratistas.find())
    return contractors


    

#@contractors_router.get("/contractors/{contractor_id}", response_model=ContractorCreate)
#async def get_contractor(contractor_id: int):
#    return buscar(contractor_id)

@contractors_router.put("/contractor/{contractor_id}", response_model=ContractorCreate)
async def update_contractor(contractor_id: int, updated_contractor: ContractorCreate):
    existing_contractor = db_client.local.contratistas.find_one({"contractor_id": contractor_id})
    if not existing_contractor:
        raise HTTPException(status_code=404, detail="Contratista no encontrado")

    # Realizar las validaciones adicionales aquí antes de actualizar el contratista
    if updated_contractor.tipo_id == "Cédula" and updated_contractor.contractor_id < 100000:
        raise HTTPException(status_code=400, detail="Número de ID inválido para Cédula")
    if updated_contractor.tipo_id == "NIT" and updated_contractor.contractor_id < 100000000:
        raise HTTPException(status_code=400, detail="Número de ID inválido para NIT")
    if updated_contractor.tipo_id_rep_legal == "Cédula" and updated_contractor.numero_id_rep_legal < 100000:
        raise HTTPException(status_code=400, detail="Número de ID del Representante Legal inválido para Cédula")
    if updated_contractor.tipo_id_rep_legal == "NIT" and updated_contractor.numero_id_rep_legal < 9:
        raise HTTPException(status_code=400, detail="Número de ID del Representante Legal inválido para NIT")

    # Actualizar las características del contratista existente con los valores proporcionados
    existing_contractor.update(updated_contractor.dict())

    # Guardar los cambios en la base de datos
    db_client.local.contratistas.replace_one({"contractor_id": contractor_id}, existing_contractor)

    return existing_contractor



@contractors_router.delete("/contractor/{contractor_id}")
async def delete_contractor(contractor_id: int):
    existing_contractor = db_client.local.contratistas.find_one({"contractor_id": contractor_id})
    if not existing_contractor:
        raise HTTPException(status_code=404, detail="Contratista no encontrado")

    # Eliminar el contratista de la base de datos
    db_client.local.contratistas.delete_one({"contractor_id": contractor_id})

    return {"message": "Contratista eliminado correctamente"}



