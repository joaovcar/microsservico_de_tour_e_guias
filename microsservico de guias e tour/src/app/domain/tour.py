from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4


@dataclass
class Passeio:
    id: UUID
    guia_id: UUID
    titulo: str
    descricao: Optional[str]
    dias: List[str]
    horarios: List[str]
    criado_em: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @staticmethod
    def criar(guia_id: UUID, titulo: str, descricao: Optional[str], dias: List[str], horarios: List[str]):
        """Fábrica para criar um novo Passeio (Tour)"""
        return Passeio(id=uuid4(), guia_id=guia_id, titulo=titulo, descricao=descricao, dias=dias, horarios=horarios)
