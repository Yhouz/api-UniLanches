from fastapi import APIRouter, HTTPException
from models import PagamentoCreate, PagamentoOut
from db import conectar_db

router = APIRouter()

@router.get("/", response_model=list[PagamentoOut])
async def listar_pagamentos():
    conn = await conectar_db()
    try:
        pagamentos = await conn.fetch("""
            SELECT 
                id_pagamento, id_pedido, status_pagamento, metodo_pagamento, valor_pago, data_pagamento, transacao_externa_id
            FROM pagamentos
        """)
        return [dict(p) for p in pagamentos]
    finally:
        await conn.close()

@router.post("/", response_model=PagamentoOut)
async def criar_pagamento(pagamento: PagamentoCreate):
    conn = await conectar_db()
    try:
        query = """
            INSERT INTO pagamentos (
                id_pedido, status_pagamento, metodo_pagamento, valor_pago, data_pagamento, transacao_externa_id
            ) VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id_pagamento, id_pedido, status_pagamento, metodo_pagamento, valor_pago, data_pagamento, transacao_externa_id
        """
        pagamento_criado = await conn.fetchrow(
            query,
            pagamento.id_pedido,
            pagamento.status_pagamento,
            pagamento.metodo_pagamento,
            pagamento.valor_pago,
            pagamento.data_pagamento,
            pagamento.transacao_externa_id
        )
        return dict(pagamento_criado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await conn.close()
