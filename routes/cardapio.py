from fastapi import APIRouter, HTTPException
from models import CardapioDoDiaCreate, CardapioDoDiaOut
from db import conectar_db
from datetime import date

router = APIRouter()

@router.get("/{data}", response_model=list[CardapioDoDiaOut])
async def buscar_cardapio(data: date):
    conn = await conectar_db()
    try:
        query = """
            SELECT * FROM cardapio_do_dia
            WHERE data = $1 AND disponivel = TRUE
            ORDER BY id_lanche
        """
        resultados = await conn.fetch(query, data)
        return [dict(r) for r in resultados]
    finally:
        await conn.close()

@router.post("/", response_model=CardapioDoDiaOut)
async def criar_cardapio(cardapio: CardapioDoDiaCreate):
    conn = await conectar_db()
    try:
        query = """
            INSERT INTO cardapio_do_dia (data, id_lanche, disponivel, observacao)
            VALUES ($1, $2, $3, $4)
            RETURNING *
        """
        registro = await conn.fetchrow(query, cardapio.data, cardapio.id_lanche, cardapio.disponivel, cardapio.observacao)
        return dict(registro)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await conn.close()
