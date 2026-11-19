import os
from contextlib import asynccontextmanager
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.orm import Session, declarative_base, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tp2.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stock = Column(Integer, nullable=False, default=0)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)


class OrderCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


def seed_products(session: Session) -> None:
    if session.scalar(select(Product).limit(1)) is not None:
        return

    session.add_all(
        Product(id=index, name=f"Produit {index}", stock=100)
        for index in range(1, 1201)
    )
    session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        seed_products(session)
    yield


app = FastAPI(title="TP2 CICD API", lifespan=lifespan)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "version": os.getenv("APP_VERSION", "dev"),
    }


@app.get("/products")
def get_products(db: Session = Depends(get_db)) -> list[dict[str, int | str]]:
    products = db.scalars(select(Product).order_by(Product.id)).all()
    return [
        {"id": product.id, "name": product.name, "stock": product.stock}
        for product in products
    ]


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)) -> dict[str, int]:
    product = db.get(Product, payload.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    if payload.quantity > product.stock:
        raise HTTPException(status_code=409, detail="Stock insuffisant")

    product.stock -= payload.quantity
    order = Order(product_id=payload.product_id, quantity=payload.quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return {
        "id": order.id,
        "product_id": order.product_id,
        "quantity": order.quantity,
    }
