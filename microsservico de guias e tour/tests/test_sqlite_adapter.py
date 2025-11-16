from uuid import uuid4

from src.app.adapters.sqlite_passeio_repositorio import RepositorioPasseioSQLite
from src.app.domain.tour import Passeio


def test_sqlite_adapter_crud(tmp_path):
    db_file = tmp_path / "test.db"
    db_url = f"sqlite:///{db_file.as_posix()}"

    repo = RepositorioPasseioSQLite(database_url=db_url)

    guia_id = uuid4()
    passeio = Passeio.criar(guia_id=guia_id, titulo="T1", descricao="D", dias=["segunda"], horarios=["09:00"])

    #create
    repo.adicionar(passeio)

    #list
    all_p = repo.listar_todos()
    assert len(all_p) == 1

    #get
    got = repo.obter(passeio.id)
    assert got is not None
    assert got.titulo == "T1"

    #update
    passeio.titulo = "T1-upd"
    repo.atualizar(passeio)
    got2 = repo.obter(passeio.id)
    assert got2 is not None
    assert got2.titulo == "T1-upd"

    #list/guia
    por_guia = repo.listar_por_guia(guia_id)
    assert any(p.id == passeio.id for p in por_guia)

    #delete
    repo.deletar(passeio.id)
    assert repo.obter(passeio.id) is None
