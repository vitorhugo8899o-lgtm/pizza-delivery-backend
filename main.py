from fastapi import FastAPI
from pedidos_rota import pedidos_rota
from autentificacao import autenti_rota


app = FastAPI() #uvicorn main:app --reload

app.include_router(pedidos_rota)
app.include_router(autenti_rota)
