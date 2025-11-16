from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.types import JSON as JSONType

from ..domain.tour import Passeio


Base = declarative_base()


class PasseioModel(Base):
    __tablename__ = "passeios"

    id = Column(String, primary_key=True, index=True)
    guia_id = Column(String, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    dias = Column(JSONType, nullable=False)
    horarios = Column(JSONType, nullable=False)
    criado_em = Column(DateTime(timezone=True), nullable=False)


class RepositorioPasseioSQLite:
    """Adapter SQLite usando SQLAlchemy (síncrono).

    Observações:
    - Usa `sqlite:///./data.db` por padrão (arquivo no workspace root).
    - `check_same_thread=False` para permitir acesso a partir de threads do uvicorn.
    """

    def __init__(self, database_url: str = "sqlite:///./data.db"):
        self.engine = create_engine(database_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        Base.metadata.create_all(bind=self.engine)

    def adicionar(self, passeio: Passeio) -> None:
        db = self.SessionLocal()
        try:
            model = PasseioModel(
                id=str(passeio.id),
                guia_id=str(passeio.guia_id),
                titulo=passeio.titulo,
                descricao=passeio.descricao,
                dias=passeio.dias,
                horarios=passeio.horarios,
                criado_em=passeio.criado_em,
            )
            db.add(model)
            db.commit()
        finally:
            db.close()

    def listar_todos(self) -> List[Passeio]:
        db = self.SessionLocal()
        try:
            rows = db.query(PasseioModel).all()
            return [self._to_domain(r) for r in rows]
        finally:
            db.close()

    def listar_por_guia(self, guia_id: UUID) -> List[Passeio]:
        db = self.SessionLocal()
        try:
            rows = db.query(PasseioModel).filter(PasseioModel.guia_id == str(guia_id)).all()
            return [self._to_domain(r) for r in rows]
        finally:
            db.close()

    def obter(self, id: UUID) -> Optional[Passeio]:
        db = self.SessionLocal()
        try:
            r = db.get(PasseioModel, str(id))
            return self._to_domain(r) if r else None
        finally:
            db.close()

    def atualizar(self, passeio: Passeio) -> None:
        db = self.SessionLocal()
        try:
            r = db.get(PasseioModel, str(passeio.id))
            if not r:
                raise KeyError("Passeio não encontrado")
            r.titulo = passeio.titulo
            r.descricao = passeio.descricao
            r.dias = passeio.dias
            r.horarios = passeio.horarios
            db.commit()
        finally:
            db.close()

    def deletar(self, id: UUID) -> None:
        db = self.SessionLocal()
        try:
            r = db.get(PasseioModel, str(id))
            if r:
                db.delete(r)
                db.commit()
        finally:
            db.close()

    def _to_domain(self, model: PasseioModel) -> Passeio:
        return Passeio(
            id=UUID(model.id),
            guia_id=UUID(model.guia_id),
            titulo=model.titulo,
            descricao=model.descricao,
            dias=list(model.dias or []),
            horarios=list(model.horarios or []),
            criado_em=model.criado_em or datetime.now(timezone.utc),
        )
