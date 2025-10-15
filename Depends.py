from sqlalchemy.orm import sessionmaker
from models import db


def pegar_sessao():
    """criar a sessão para o banco de dados com a garantia de que ela feche indenpendete do que acontecer"""
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
        