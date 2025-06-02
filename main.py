from fastapi import FastAPI
from routes import pagamentos, usuarios, lanches, pedidos, itens_pedido, cardapio
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="API UniLanches")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem. Para produção, use ["https://seuapp.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE...)
    allow_headers=["*"],  # Permite todos os headers
)

app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(lanches.router, prefix="/lanches", tags=["Lanches"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(itens_pedido.router, prefix="/itens_pedido", tags=["ItensPedido"])
app.include_router(cardapio.router, prefix="/cardapio", tags=["CardapioDoDia"])
app.include_router(pagamentos.router, prefix="/pagamentos", tags=["Pagamentos"])


