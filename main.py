from fastapi import FastAPI
from routes import usuarios, lanches, pedidos, itens_pedido, cardapio

app = FastAPI(title="API UniLanches")

app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(lanches.router, prefix="/lanches", tags=["Lanches"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(itens_pedido.router, prefix="/itens_pedido", tags=["ItensPedido"])
app.include_router(cardapio.router, prefix="/cardapio", tags=["CardapioDoDia"])
