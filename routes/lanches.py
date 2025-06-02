from fastapi import APIRouter, HTTPException
from models import LancheCreate, LancheOut
from db import conectar_db

router = APIRouter()

@router.get("/", response_model=list[LancheOut])
async def listar_lanches():
    conn = await conectar_db()
    try:
        lanches = await conn.fetch("SELECT * FROM lanches WHERE ativo = TRUE ORDER BY nome")
        return [dict(l) for l in lanches]
    finally:
        await conn.close()

@router.post("/", response_model=LancheOut)
async def criar_lanche(lanche: LancheCreate):
    conn = await conectar_db()
    try:
        query = """
            INSERT INTO lanches (nome, descricao, preco, ativo)
            VALUES ($1, $2, $3, $4)
            RETURNING *
        """
        lanche_criado = await conn.fetchrow(query, lanche.nome, lanche.descricao, lanche.preco, lanche.ativo)
        return dict(lanche_criado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await conn.close()
