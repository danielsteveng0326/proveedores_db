from fastapi import APIRouter, HTTPException
from typing import List
from db.models.schemas import ContractorCreate
from db.client import db_client
from db.models.schemas import ContractorCreate

contractors_router = APIRouter()



@contractors_router.get("/")
async def get_home():
    return {"message":"Bienvenido a la API de contratos y contratistas"}

@contractors_router.post("/contractors", response_model=ContractorCreate)
async def create_contractor(contractor: ContractorCreate):
        if buscar(contractor.contractor_id) is not None:
            raise HTTPException(status_code=400, detail="El contratista ya existe")
    
    # Realizar las validaciones adicionales aquí antes de guardar el contratista
        if contractor.tipo_id == "Cédula" and contractor.contractor_id < 100000:
            raise HTTPException(status_code=400, detail="Número de ID inválido para Cédula")
        if contractor.tipo_id == "NIT" and contractor.contractor_id != 9:
            raise HTTPException(status_code=400, detail="Número de ID inválido para NIT")
        if contractor.tipo_id_rep_legal == "Cédula" and contractor.numero_id_rep_legal < 100000:
            raise HTTPException(status_code=400, detail="Número de ID del Representante Legal inválido para Cédula")
        if contractor.tipo_id_rep_legal == "NIT" and contractor.numero_id_rep_legal != 9:
            raise HTTPException(status_code=400, detail="Número de ID del Representante Legal inválido para NIT")
        
        contr_dict = dict(contractor)
        
        db_client.local.contratistas.insert_one(contr_dict)

        return contractor

@contractors_router.get("/contractors", response_model=List[ContractorCreate])
async def get_contractors():
    return contractors

@contractors_router.get("/contractors/{contractor_id}", response_model=ContractorCreate)
async def get_contractor(contractor_id: int):
    return buscar(contractor_id)

@contractors_router.put("/contractors/{contractor_id}", response_model=ContractorCreate)
async def update_contractor(contractor_id: int, contractor: ContractorCreate):
    for index, contractor_modificat in enumerate(contractors):
        if contractor_modificat["contractor_id"] == contractor_id:
            contractors[index] = contractor
            return contractor
    raise HTTPException(status_code=404, detail="Contractor not found")


@contractors_router.delete("/contractors/{contractor_id}")
async def delete_contractor(contractor_id: int):
    for index, contractor in enumerate(contractors):
        if contractor["contractor_id"] == contractor_id:
            contractors.pop(index)
            return {"message": "Contractor deleted", "contractor": contractor}
    raise HTTPException(status_code=404, detail="Contractor not found")



def buscar(contractor_id: int):
    contractor = next((c for c in contractors if c["contractor_id"] == contractor_id), None)
    return contractor



