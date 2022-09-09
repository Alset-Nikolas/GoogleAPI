from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import (
    Integer,
    String,
    Column,
    create_engine,
    ForeignKeyConstraint,
    UniqueConstraint,
    Boolean,
    func,
    cast,
    Index,
    Date,
    Float,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.operators import op

DATABASE = {
    "drivername": "postgresql",
    # "host": "postgres",
    "host": "localhost",
    "port": "5432",
    "username": "postgres",
    "password": "qwerty",
    "database": "db_orders",
}
Base = declarative_base()
engine = create_engine(
    f'postgresql+psycopg2://{DATABASE["username"]}:{DATABASE["password"]}@{DATABASE["host"]}:{DATABASE["port"]}/{DATABASE["database"]}'
)


session = Session(bind=engine)


class OrederModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_number = Column(Integer, nullable=False, unique=True)
    price_dollar = Column(Integer, nullable=False)
    price_rub = Column(Float, nullable=False)
    delivery_date = Column(Date, nullable=False)
