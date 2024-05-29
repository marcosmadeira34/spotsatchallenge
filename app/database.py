from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

user = os.environ.get("USER")
password = os.environ.get("PASSWORD")
host = os.environ.get("HOST")
port = os.environ.get("PORT")

# Definir o endereço do banco de dados com o usuário, senha e nome do banco de dados
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/geodb"


engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
