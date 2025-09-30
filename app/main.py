
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models, schemas
from .security import verify_password, create_token
from .deps import get_current_user

app = FastAPI(title="Biblioteca Nuevo Milenio API", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    token = create_token(user.username)
    return schemas.TokenResponse(access_token=token, full_name=user.full_name)

@app.get("/books", response_model=list[schemas.BookDTO])
def list_books(q: str | None = Query(None, description="Filtro de búsqueda"), db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    query = db.query(models.Book)
    if q:
        like = f"%{q}%"
        query = query.filter((models.Book.title.ilike(like)) | (models.Book.author.ilike(like)))
    books = query.order_by(models.Book.title.asc()).all()
    return [schemas.BookDTO.model_validate(b) for b in books]

@app.post("/books/{book_id}/borrow", response_model=schemas.BookDTO)
def borrow_book(book_id: int, payload: schemas.BorrowRequest, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    book = db.query(models.Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if book.is_borrowed:
        raise HTTPException(status_code=409, detail="El libro ya está prestado")
    book.is_borrowed = True
    book.borrowed_by = payload.borrower_name
    db.add(book)
    db.commit()
    db.refresh(book)
    return schemas.BookDTO.model_validate(book)

@app.post("/books/{book_id}/return", response_model=schemas.BookDTO)
def return_book(book_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    book = db.query(models.Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if not book.is_borrowed:
        raise HTTPException(status_code=409, detail="El libro ya está disponible")
    book.is_borrowed = False
    book.borrowed_by = None
    db.add(book)
    db.commit()
    db.refresh(book)
    return schemas.BookDTO.model_validate(book)
