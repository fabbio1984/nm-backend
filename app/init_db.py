
from .database import Base, engine, SessionLocal
from .models import User, Book
from .security import hash_password

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # seed admin
    if not db.query(User).filter_by(username="admin").first():
        admin = User(username="admin", full_name="Administrador", password_hash=hash_password("admin123"))
        db.add(admin)
    # seed books
    if not db.query(Book).first():
        demo = [
            Book(title="Cien años de soledad", author="G. García Márquez"),
            Book(title="El amor en los tiempos del cólera", author="G. García Márquez"),
            Book(title="Don Quijote de la Mancha", author="Miguel de Cervantes"),
            Book(title="La metamorfosis", author="Franz Kafka"),
        ]
        db.add_all(demo)
    db.commit()
    db.close()
    print("DB inicializada con usuario admin/admin123 y 4 libros.")

if __name__ == "__main__":
    run()
