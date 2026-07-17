# crud_fastapi
Projeto simples para aprender FastAPI + SQLAlchemy com um CRUD completo.

## O que tem aqui
- API REST com FastAPI
- Banco SQLite com SQLAlchemy
- Operações CRUD: criar, listar, buscar, atualizar e deletar
- Código comentado para facilitar o aprendizado

## Como rodar
1. Instale as dependências:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic
   ```
2. Inicie a aplicação:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Abra o navegador em:
   - http://127.0.0.1:8000/docs

## Endpoints disponíveis
- GET /
- POST /items
- GET /items
- GET /items/{item_id}
- PUT /items/{item_id}
- DELETE /items/{item_id}
