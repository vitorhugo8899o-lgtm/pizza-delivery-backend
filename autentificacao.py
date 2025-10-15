from fastapi import APIRouter,Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from Depends import pegar_sessao
from schemas import UsarioSchema, LoginSchema
from models import Usuario 
from security import hash_senha, verificar_senha, criar_access_token, timedelta



autenti_rota = APIRouter(prefix='/auth',tags=['Autentificação'])

@autenti_rota.post("/Criar_conta")
async def criar_conta(usuario_schema:UsarioSchema, session=Depends(pegar_sessao)):
    """Endpoint para a criação da conta, retorna um erro se o email do usuario já tiver cadastrado"""
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(
            status_code=409, detail="Usuário já cadastrado com esse email!"
        )
    else:
        senha_hashed = hash_senha(usuario_schema.senha)
        novo_usuario = Usuario(
            user_name=usuario_schema.user_name,
            email=usuario_schema.email,
            senha=senha_hashed,
            adm=usuario_schema.adm 
        )

        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)

        return {'mensagem':f'Usuário {usuario_schema.user_name} cadastrado com sucesso!, bem vindo.'}

@autenti_rota.post("/Login")
async def Logar(form_data: OAuth2PasswordRequestForm = Depends(),session=Depends(pegar_sessao)):
    """Endpoint para login, faz uma verificação da senha, que seja incorreta retorna um erro"""
    usuario = session.query(Usuario).filter(Usuario.email == form_data.username).first()
    

    if not usuario or not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(
            status_code=401, detail="E-mail ou senha incorretos."
        )

    access_token_expires = timedelta(minutes=30) 
    access_token = criar_access_token(
        data={"sub": usuario.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "mensagem": f'Login bem-sucedido. Bem-vindo(a), {usuario.user_name}!'
    }
    
