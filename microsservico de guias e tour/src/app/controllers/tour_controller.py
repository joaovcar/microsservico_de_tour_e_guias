from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List
from uuid import UUID

from ..schemas.tour_schema import PasseioCriarDTO, PasseioDTO
from ..usecases.tour_usecase import PasseioUseCase
from ..domain.tour import Passeio

router = APIRouter()


def get_usecase(request: Request) -> PasseioUseCase:
    repo = getattr(request.app.state, "repositorio", None)
    if repo is None:
        raise RuntimeError("Repositório não configurado na aplicação")
    return PasseioUseCase(repo)


@router.post("/guias/{guia_id}/passeios", response_model=PasseioDTO, status_code=status.HTTP_201_CREATED)
def criar_passeio(guia_id: UUID, dto: PasseioCriarDTO, usecase: PasseioUseCase = Depends(get_usecase)):
    passeio = usecase.criar_passeio(guia_id=guia_id, titulo=dto.titulo, descricao=dto.descricao, dias=dto.dias, horarios=dto.horarios)
    return {
        "id": str(passeio.id),
        "guia_id": str(passeio.guia_id),
        "titulo": passeio.titulo,
        "descricao": passeio.descricao,
        "dias": passeio.dias,
        "horarios": passeio.horarios,
    }


@router.get("/passeios", response_model=List[PasseioDTO])
def listar_passeios(usecase: PasseioUseCase = Depends(get_usecase)):
    passeios = usecase.listar_passeios()
    return [
        {
            "id": str(t.id),
            "guia_id": str(t.guia_id),
            "titulo": t.titulo,
            "descricao": t.descricao,
            "dias": t.dias,
            "horarios": t.horarios,
        }
        for t in passeios
    ]


@router.get("/guias/{guia_id}/passeios", response_model=List[PasseioDTO])
def listar_passeios_por_guia(guia_id: UUID, usecase: PasseioUseCase = Depends(get_usecase)):
    passeios = usecase.listar_passeios_por_guia(guia_id)
    return [
        {
            "id": str(t.id),
            "guia_id": str(t.guia_id),
            "titulo": t.titulo,
            "descricao": t.descricao,
            "dias": t.dias,
            "horarios": t.horarios,
        }
        for t in passeios
    ]


@router.get("/passeios/{passeio_id}", response_model=PasseioDTO)
def obter_passeio(passeio_id: UUID, usecase: PasseioUseCase = Depends(get_usecase)):
    t = usecase.obter_passeio(passeio_id)
    if not t:
        raise HTTPException(status_code=404, detail="Passeio não encontrado")
    return {
        "id": str(t.id),
        "guia_id": str(t.guia_id),
        "titulo": t.titulo,
        "descricao": t.descricao,
        "dias": t.dias,
        "horarios": t.horarios,
    }


@router.put("/passeios/{passeio_id}", response_model=PasseioDTO)
def atualizar_passeio(passeio_id: UUID, dto: PasseioCriarDTO, usecase: PasseioUseCase = Depends(get_usecase)):
    existente = usecase.obter_passeio(passeio_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Passeio não encontrado")
    atualizado = Passeio(id=existente.id, guia_id=existente.guia_id, titulo=dto.titulo, descricao=dto.descricao, dias=dto.dias, horarios=dto.horarios)
    usecase.atualizar_passeio(atualizado)
    return {
        "id": str(atualizado.id),
        "guia_id": str(atualizado.guia_id),
        "titulo": atualizado.titulo,
        "descricao": atualizado.descricao,
        "dias": atualizado.dias,
        "horarios": atualizado.horarios,
    }


@router.delete("/passeios/{passeio_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_passeio(passeio_id: UUID, usecase: PasseioUseCase = Depends(get_usecase)):
    existente = usecase.obter_passeio(passeio_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Passeio não encontrado")
    usecase.deletar_passeio(passeio_id)
    return None
