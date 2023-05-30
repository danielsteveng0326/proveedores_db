from fastapi import APIRouter, HTTPException
from typing import List
from schemas import ContractorCreate

contractors_router = APIRouter()
contractors =  [

    {
        "nombre_razon_social": "Ana Maria Torres",
        "tipo_id": "Cédula",
        "contractor_id": 1087654321,
        "nombre_rep_legal": "Ana Maria Torres",
        "tipo_id_rep_legal": "Cédula",
        "numero_id_rep_legal": 1087654321,
        "fecha_expedicion_cedula": "15/07/2005",
        "departamento_expedicion_cedula": "Valle del Cauca",
        "municipio_expedicion_cedula": "Cali",
        "direccion": "Avenida Principal #123",
        "telefono": "3332225555",
        "correo_electronico": "ana@maria.com",
        "fecha_nacimiento": "12/02/1987",
        "departamento_nacimiento": "Valle del Cauca",
        "municipio_nacimiento": "Cali"
    },

    {
        "nombre_razon_social": "Juan Pérez",
        "tipo_id": "Cédula",
        "contractor_id": 1234567890,
        "nombre_rep_legal": "Juan Pérez",
        "tipo_id_rep_legal": "Cédula",
        "numero_id_rep_legal": 1234567890,
        "fecha_expedicion_cedula": "20/05/2010",
        "departamento_expedicion_cedula": "Bogotá",
        "municipio_expedicion_cedula": "Bogotá",
        "direccion": "Calle Principal #456",
        "telefono": "1112223333",
        "correo_electronico": "juan@perez.com",
        "fecha_nacimiento": "01/01/1990",
        "departamento_nacimiento": "Cundinamarca",
        "municipio_nacimiento": "Bogotá"
    },

    {
        "nombre_razon_social": "María Rodríguez",
        "tipo_id": "Cédula",
        "contractor_id": 9876543210,
        "nombre_rep_legal": "María Rodríguez",
        "tipo_id_rep_legal": "Cédula",
        "numero_id_rep_legal": 9876543210,
        "fecha_expedicion_cedula": "10/03/2008",
        "departamento_expedicion_cedula": "Antioquia",
        "municipio_expedicion_cedula": "Medellín",
        "direccion": "Carrera Principal #789",
        "telefono": "4445556666",
        "correo_electronico": "maria@rodriguez.com",
        "fecha_nacimiento": "15/06/1985",
        "departamento_nacimiento": "Antioquia",
        "municipio_nacimiento": "Medellín"
    },

    {
        "nombre_razon_social": "Carlos Gómez",
        "tipo_id": "Cédula",
        "contractor_id": 2468135790,
        "nombre_rep_legal": "Carlos Gómez",
        "tipo_id_rep_legal": "Cédula",
        "numero_id_rep_legal": 2468135790,
        "fecha_expedicion_cedula": "05/09/2007",
        "departamento_expedicion_cedula": "Atlántico",
        "municipio_expedicion_cedula": "Barranquilla",
        "direccion": "Avenida Principal #987",
        "telefono": "7778889999",
        "correo_electronico": "carlos@gomez.com",
        "fecha_nacimiento": "25/12/1982",
        "departamento_nacimiento": "Atlántico",
        "municipio_nacimiento": "Barranquilla"
    },


    {
        "nombre_razon_social": "Luisa Hernández",
        "tipo_id": "Cédula",
        "contractor_id": 1357924680,
        "nombre_rep_legal": "Luisa Hernández",
        "tipo_id_rep_legal": "Cédula",
        "numero_id_rep_legal": 1357924680,
        "fecha_expedicion_cedula": "18/11/2006",
        "departamento_expedicion_cedula": "Valle del Cauca",
        "municipio_expedicion_cedula": "Cali",
        "direccion": "Calle Principal #321",
        "telefono": "8889990000",
        "correo_electronico": "luisa@hernandez.com",
        "fecha_nacimiento": "08/07/1992",
        "departamento_nacimiento": "Valle del Cauca",
        "municipio_nacimiento": "Cali"
    },


    {
        "nombre_razon_social": "Pedro López",
        "tipo_id": "Cédula",
        "contractor_id": 3698521470,
        "nombre_rep_legal": "Pedro López",
        "tipo_id_rep_legal": "Cédula",
        "numero_id_rep_legal": 3698521470,
        "fecha_expedicion_cedula": "30/04/2009",
        "departamento_expedicion_cedula": "Santander",
        "municipio_expedicion_cedula": "Bucaramanga",
        "direccion": "Carrera Principal #654",
        "telefono": "2223334444",
        "correo_electronico": "pedro@lopez.com",
        "fecha_nacimiento": "10/10/1988",
        "departamento_nacimiento": "Santander",
        "municipio_nacimiento": "Bucaramanga"
    },
]

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
        
        contractors.append(contractor.dict())
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



