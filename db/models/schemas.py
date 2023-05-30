from enum import Enum
from pydantic import BaseModel, Field

class IDTypeEnum(str, Enum):
    CEDULA = "Cédula"
    NIT = "NIT"
    PASAPORTE = "Pasaporte"

class ContractorCreate(BaseModel):
    nombre_razon_social: str = Field(..., min_length=2)
    tipo_id: IDTypeEnum
    contractor_id: int
    nombre_rep_legal: str = Field(..., min_length=5)
    tipo_id_rep_legal: IDTypeEnum
    numero_id_rep_legal: int
    fecha_expedicion_cedula: str
    departamento_expedicion_cedula: str
    municipio_expedicion_cedula: str
    direccion: str
    telefono: str
    correo_electronico: str
    fecha_nacimiento: str
    departamento_nacimiento: str
    municipio_nacimiento: str
