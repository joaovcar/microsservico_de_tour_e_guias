from typing import List, Optional
from uuid import UUID
from ..domain.tour import Passeio
from ..repositories.tour_repository import IPasseioRepositorio


class PasseioUseCase:
    """Lógica de negócio para passeios."""

    def __init__(self, repo: IPasseioRepositorio):
        self.repo = repo

    def criar_passeio(self, guia_id: UUID, titulo: str, descricao: Optional[str], dias: List[str], horarios: List[str]) -> Passeio:
        passeio = Passeio.criar(guia_id=guia_id, titulo=titulo, descricao=descricao, dias=dias, horarios=horarios)
        self.repo.adicionar(passeio)
        return passeio

    def listar_passeios(self) -> List[Passeio]:
        return self.repo.listar_todos()

    def listar_passeios_por_guia(self, guia_id: UUID) -> List[Passeio]:
        return self.repo.listar_por_guia(guia_id)

    def obter_passeio(self, id: UUID) -> Optional[Passeio]:
        return self.repo.obter(id)

    def atualizar_passeio(self, passeio: Passeio) -> None:
        self.repo.atualizar(passeio)

    def deletar_passeio(self, id: UUID) -> None:
        self.repo.deletar(id)
