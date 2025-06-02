from fastapi import APIRouter, HTTPException
from models import ItemPedidoCreate, ItemPedidoOut
from db import conectar_db

router = APIRouter()

@router.get("/", response_model=list[ItemPedidoOut])
async def listar_itens():
    conn = await conectar_db()
    try:
        itens = await conn.fetch("SELECT * FROM itens_pedido")
        return [dict(i) for i in itens]
    finally:
        await conn.close()

@router.post("/", response_model=ItemPedidoOut)
async def criar_item(item: ItemPedidoCreate):
    conn = await conectar_db()
    try:
        query = """
            INSERT INTO itens_pedido (id_pedido, id_lanche, quantidade)
            VALUES ($1, $2, $3)
            RETURNING *
        """
        item_criado = await conn.fetchrow(query, item.id_pedido, item.id_lanche, item.quantidade)
        return dict(item_criado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await conn.close()
