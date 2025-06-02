from fastapi import APIRouter, HTTPException
from models import UsuarioCreate, UsuarioOut
from db import conectar_db

router = APIRouter()

@router.get("/", response_model=list[UsuarioOut])
async def listar_usuarios():
    conn = await conectar_db()
    try:
        usuarios = await conn.fetch("SELECT id_usuario, nome, email, cpf, telefone, tipo_usuario, saldo_carteira FROM usuarios")
        return [dict(u) for u in usuarios]
    finally:
        await conn.close()

@router.post("/", response_model=UsuarioOut)
async def criar_usuario(usuario: UsuarioCreate):
    conn = await conectar_db()
    try:
        query = """
            INSERT INTO usuarios (nome, email, senha, cpf, telefone, tipo_usuario)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id_usuario, nome, email, cpf, telefone, tipo_usuario, saldo_carteira
        """
        usuario_criado = await conn.fetchrow(query, usuario.nome, usuario.email, usuario.senha, usuario.cpf, usuario.telefone, usuario.tipo_usuario)
        return dict(usuario_criado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await conn.close()
