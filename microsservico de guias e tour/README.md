# Microsserviço de Guias e Passeios 
Pequeno microsserviço que permite que guias criem, listem, atualizem e deletem passeios oferecidos por eles. Segue princípios de Clean Architecture: entidades em `domain/`, regras em `usecases/`, contratos em `repositories/` e adaptadores em `adapters/`.

Início rápido (PowerShell):

```powershell
#Ativar o virtualenv existente 
.\venv\Scripts\Activate.ps1

#Instalar dependências
pip install -r requirements.txt

#Rodar a aplicação com uvicorn 
uvicorn src.app.main:app --reload --port 8000 --reload-dir src

#Rodar os testes
pytest -q

#Ao finalizar
deactivate
```

Rodando com Docker + Nginx (produção local)

 - Atualize `deploy/nginx.conf` e substitua `server_name example.com` pelo seu domínio.
 - O `docker-compose.yml` cria dois serviços: `app` (Gunicorn+Uvicorn) e `nginx`.

Para executar (é necessário ter Docker e Docker Compose instalados):

```powershell
docker compose build
docker compose up -d
```

O Nginx ficará disponível na porta 80 do host e irá encaminhar para o serviço `app`.

Observação sobre TLS: para habilitar HTTPS em produção, use um reverse proxy com Certbot (Let's Encrypt) ou um serviço de terminador TLS.

HTTPS automático com Let's Encrypt (docker)

Você pode usar `nginx-proxy` + `letsencrypt-nginx-proxy-companion` para obter certificados TLS automaticamente.

1. Edite `deploy/docker-compose.letsencrypt.yml` e substitua `example.com` e `you@example.com` pelas suas configurações reais (`VIRTUAL_HOST` e `LETSENCRYPT_EMAIL`).
2. Suba o stack combinando os arquivos:

```powershell
docker compose -f docker-compose.yml -f deploy/docker-compose.letsencrypt.yml up -d --build
```

O proxy (`jwilder/nginx-proxy`) publicará porta 80/443 e o companion (`jrcs/letsencrypt-nginx-proxy-companion`) solicitará/renovará certificados automaticamente.

Importante: seu domínio deve apontar para o IP do host (DNS A record) antes de executar para que o Let's Encrypt possa validar os desafios.


Rotas principais:

- POST /guias/{guia_id}/passeios - criar um passeio para o guia
- GET /passeios - listar todos os passeios
- GET /guias/{guia_id}/passeios - listar passeios de um guia
- GET /passeios/{passeio_id} - obter detalhe de um passeio
- PUT /passeios/{passeio_id} - atualizar passeio
- DELETE /passeios/{passeio_id} - deletar passeio

Estrutura do projeto (principais pastas):

- `src/app/domain` - Entidades (modelo de domínio)
- `src/app/usecases` - Regras de negócio (casos de uso)
- `src/app/repositories` - Contrato do repositório (Protocol)
- `src/app/adapters` - Implementações do repositório (ex.: em memória)
- `src/app/controllers` - Rotas FastAPI

Observações
- Persistência: o projeto agora inclui um adaptador SQLite usando SQLAlchemy. Por padrão a aplicação usa SQLite e cria o arquivo `data.db` na raiz do workspace.
- Para forçar o uso do repositório em memória (útil em testes) exporte a variável de ambiente `PERSISTENCE=memory` antes de iniciar a aplicação.
- As mensagens e rotas foram traduzidas para português — isso altera a API (breaking change). Atualize clientes conforme necessário.
