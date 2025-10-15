from pydantic import BaseModel, EmailStr
from typing import Optional

#optei por padronizar os parâmetros que eu fosse passar

class UsarioSchema(BaseModel):
    user_name : str
    nome : str
    email : EmailStr
    senha : str
    adm : Optional[bool] = False

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True


class PedidoSchama(BaseModel):
    id_pizza : str
    preco : float
    pago : bool

    class Config:
        from_attributes = True

class PizzaSchema(BaseModel):
    sabor : str
    tamanho : str
    preco_unid : float

    class Config:
        from_attributes = True
        