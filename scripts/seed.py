import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.main import Base, Product


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tp2.db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def seed() -> int:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        existing = session.scalar(select(Product).limit(1))
        if existing is not None:
            return session.query(Product).count()

        session.add_all(
            Product(id=index, name=f"Produit {index}", stock=100)
            for index in range(1, 1201)
        )
        session.commit()
        return session.query(Product).count()


if __name__ == "__main__":
    print(f"{seed()} produits initialises")
