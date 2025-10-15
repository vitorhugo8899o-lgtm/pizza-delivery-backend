from fastapi import APIRouter,Depends, HTTPException
from Depends import pegar_sessao 
from models import Usuario, Pizza, Pedidos
from Login_Depnds import get_usuario_logado 
from schemas import PizzaSchema, PedidoSchama


pedidos_rota = APIRouter(prefix='/Pedido',tags=['Pedidos'])

@pedidos_rota.get('/Cardapio')
async def cardapio(session=Depends(pegar_sessao)):
    """Endpoint do cardapio, faz a busca das pizzas que tem no Banco de daos e retona todos os dados"""
    pesguisa = session.query(Pizza).all() 

    return {"mensagem": f'Seja bem vindo, Cardápio completo!', "cardapio": pesguisa}


@pedidos_rota.post('/Fazer_Pedido')
async def fazer_pedido(pedido_schema:PedidoSchama,usuario_logado:Usuario = Depends(get_usuario_logado),session=Depends(pegar_sessao)):
    """Endpoint para fazer pedidos"""
    if usuario_logado.adm == True:
        raise HTTPException(
            status_code=401,detail='Usuários adiministradores não podem fazer pedidos nas contas adm, por favor utilize sua conta pessoal.'
        )
    else:
        novo_pedido = Pedidos(
            id_usuario=usuario_logado.id,
            id_pizza=pedido_schema.id_pizza,
            preco=pedido_schema.preco,
            pago=pedido_schema.pago)
        
        
        session.add(novo_pedido)
        session.commit()
        session.refresh(novo_pedido)
        
        return {'mensagem':f'Pedido efetuado, Por favor aguarde atualizações!'}


@pedidos_rota.post("/Produto")
async def adionar_sabor(pizza_schema:PizzaSchema,usuario_logado: Usuario = Depends(get_usuario_logado),session=Depends(pegar_sessao)):
    """Endpoint para cadastrar sabores de pizzas com validação para saber se o usario é adm"""
    
    
    if usuario_logado.adm == True:
        add_sabor = Pizza(
            sabor = pizza_schema.sabor,
            tamanho = pizza_schema.tamanho,
            preco_unid = pizza_schema.preco_unid
        )

        pesquisa = session.query(Pizza).filter(Pizza.sabor==pizza_schema.sabor).first()
        if pesquisa:
            raise {'mensagem':'Sabor de pizza já cadastrada no sistema'}
        else:
            session.add(add_sabor)
            session.commit()
            session.refresh(add_sabor)
            
            return {'mensagem':'Novo sabor de pizza adicionado no sistema'}

    else:
        raise HTTPException(
            status_code=401,
            detail='Usuário não é um adiministrador'
        )
