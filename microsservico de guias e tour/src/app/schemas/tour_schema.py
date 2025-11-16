from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from uuid import UUID


class PasseioCriarDTO(BaseModel):
    titulo: str = Field(..., json_schema_extra={"example": "Passeio a pé pela cidade"})
    descricao: Optional[str] = Field(None, json_schema_extra={"example": "Um passeio relaxante pelo centro histórico."})
    dias: List[str] = Field(..., json_schema_extra={"example": ["segunda", "quarta", "sexta"]})
    horarios: List[str] = Field(..., json_schema_extra={"example": ["09:00", "14:00"]})


class PasseioDTO(PasseioCriarDTO):
    id: UUID
    guia_id: UUID

    model_config = ConfigDict(from_attributes=True)
