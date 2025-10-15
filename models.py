from sqlalchemy import create_engine, Column, String, Float, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base


db = create_engine("sqlite:///banco.db")
Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column("id",Integer, primary_key=True, autoincrement=True)
    user_name = Column("user_name",String)
    email = Column("email",String,nullable=False)
    senha = Column("senha",String,nullable=False)
    adm = Column("adm",Boolean, default=False)

    def __init__(self, user_name, email, senha, adm=False):

        self.user_name = user_name
        self.email = email
        self.senha = senha
        self.adm = adm
        



class Pedidos(Base):
    __tablename__ = 'pedidos'

    id = Column("id",Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario",ForeignKey("usuario.id"), nullable=False)
    id_pizza = Column("id_pizza",ForeignKey("pizza.id"), nullable=False)
    preco = Column("preco",Float, nullable=False)
    pago = Column("pago",Boolean,nullable=False)

    def __init__(self,id_usuario,id_pizza,preco,pago):
        self.id_usuario = id_usuario
        self.id_pizza = id_pizza
        self.preco = preco
        self.pago = pago


class Pizza(Base):
    __tablename__ = "pizza"

    id = Column("id",Integer, primary_key=True, autoincrement=True)
    sabor = Column("sabor",String,nullable=True)
    tamanho = Column("tamanho",String,nullable=False)
    preco_unid = Column("preco_unid",Float,nullable=False)

    def __init__(self,sabor,tamanho,preco_unid,):
        self.sabor = sabor 
        self.tamanho = tamanho
        self.preco_unid = preco_unid
