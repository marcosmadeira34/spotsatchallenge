from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, JSON
from databases import Database
import os

user = os.environ.get("USER")
password = os.environ.get("PASSWORD")
host = os.environ.get("HOST")
port = os.environ.get("PORT")

# Definir o endereço do banco de dados com o usuário, senha e nome do banco de dados
DATABASE_URL = f"postgresql://postgres:postgres@localhost:5432"

database = Database(DATABASE_URL)
metadata = MetaData()

Graph = Table(
    "graphs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("data", JSON),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
