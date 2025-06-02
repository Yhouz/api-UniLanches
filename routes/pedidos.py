from fastapi import APIRouter, HTTPException
from models import PedidoCreate, PedidoOut
from db import conectar_db

router = APIRouter()

@router.get("/", response_model=list[PedidoOut])
async def listar_pedidos():
    conn = await conectar_db()
    try:
        pedidos = await conn.fetch("SELECT * FROM pedidos ORDER BY data_pedido DESC")
        return [dict(p) for p in pedidos]
    finally:
        await conn.close()

@router.post("/", response_model=PedidoOut)
async def criar_pedido(pedido: PedidoCreate):
    conn = await conectar_db()
    try:
        query = """
            INSERT INTO pedidos (id_usuario, valor_total, forma_pagamento, status, data_pedido)
            VALUES ($1, $2, $3, $4, COALESCE($5, NOW()))
            RETURNING *
        """
        pedido_criado = await conn.fetchrow(query, pedido.id_usuario, pedido.valor_total, pedido.forma_pagamento, pedido.status, pedido.data_pedido)
        return dict(pedido_criado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await conn.close()
