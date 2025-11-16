from fastapi import FastAPI
import os
import sys

from .controllers.tour_controller import router as tour_router


def create_app() -> FastAPI:
    app = FastAPI(title="Microsserviço de guia de tour", version="0.1.0")
    
    if os.environ.get("PERSISTENCE"):
        persistence = os.environ.get("PERSISTENCE").lower()
    elif "PYTEST_CURRENT_TEST" in os.environ or "pytest" in sys.modules:
        persistence = "memory"
    else:
        persistence = "sqlite"

    if persistence == "sqlite":
        from .adapters.sqlite_passeio_repositorio import RepositorioPasseioSQLite

        app.state.repositorio = RepositorioPasseioSQLite(database_url=os.environ.get("DATABASE_URL", "sqlite:///./data.db"))
    else:
        #fallback para memória )
        from .adapters.inmemory_tour_repository import RepositorioPasseioMemoria

        app.state.repositorio = RepositorioPasseioMemoria()

    app.include_router(tour_router)
    return app


app = create_app()
