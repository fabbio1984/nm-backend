
# Backend FastAPI — Biblioteca Nuevo Milenio

Endpoints principales:
- `POST /auth/login` — retorna token simple (demo) si las credenciales son válidas.
- `GET /books` — lista de libros; filtra con `?q=texto`.
- `POST /books/{id}/borrow` — presta libro.
- `POST /books/{id}/return` — devuelve libro.

## Variables de entorno
- `DATABASE_URL` (Render la entrega automáticamente) ejemplo local: `postgresql+psycopg2://postgres:postgres@localhost:5432/biblioteca`
- `SECRET_KEY` (cualquier string; aquí se usa para firmar tokens simples de demo)

## Desarrollo local
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/biblioteca"
export SECRET_KEY="cambia-esto"
python -m app.init_db  # crea tablas y datos demo
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Despliegue en Render (resumen)
1. Crea **PostgreSQL** en Render.
2. Crea **Web Service** desde este repo (Python).
3. En *Environment* agrega:
   - `DATABASE_URL` (Render provee automáticamente si linkeas la BD)
   - `SECRET_KEY=algo-super-secreto`
4. **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port 10000`
5. Ejecuta una vez `python -m app.init_db` en un Shell de Render para crear tablas y datos demo.
