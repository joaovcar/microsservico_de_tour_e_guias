from typing import Dict, List, Optional
from uuid import UUID
from ..domain.tour import Passeio


class RepositorioPasseioMemoria:
    """Repositório em memória simples. Adapter implementando o contrato do repositório.
    Não é thread-safe; substitua por persistência real quando necessário.
    """

    def __init__(self):
        self._store: Dict[UUID, Passeio] = {}

    def adicionar(self, passeio: Passeio) -> None:
        self._store[passeio.id] = passeio

    def listar_todos(self) -> List[Passeio]:
        return list(self._store.values())

    def listar_por_guia(self, guia_id: UUID) -> List[Passeio]:
        return [t for t in self._store.values() if t.guia_id == guia_id]

    def obter(self, id: UUID) -> Optional[Passeio]:
        return self._store.get(id)

    def atualizar(self, passeio: Passeio) -> None:
        if passeio.id in self._store:
            self._store[passeio.id] = passeio
        else:
            raise KeyError("Passeio não encontrado")

    def deletar(self, id: UUID) -> None:
        self._store.pop(id, None)
