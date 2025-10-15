from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from security import decodificar_token 
from models import Usuario 
from Depends import pegar_sessao 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/Login")

async def get_usuario_logado(token: str = Depends(oauth2_scheme),session: Session =Depends(pegar_sessao)):

    email = decodificar_token(token)
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais de autenticação inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return usuario 
