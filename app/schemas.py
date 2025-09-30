
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    full_name: str | None = None

class BookDTO(BaseModel):
    id: int
    title: str
    author: str | None = None
    is_borrowed: bool
    borrowed_by: str | None = None

    class Config:
        from_attributes = True

class BorrowRequest(BaseModel):
    borrower_name: str
