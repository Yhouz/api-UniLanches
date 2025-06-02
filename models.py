from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime

class UsuarioBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    telefone: Optional[str]
    tipo_usuario: str  # cliente, funcionario, admin

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioOut(UsuarioBase):
    id_usuario: int
    saldo_carteira: float

    class Config:
        orm_mode = True

class LancheBase(BaseModel):
    nome: str
    descricao: Optional[str]
    preco: float
    ativo: Optional[bool] = True

class LancheCreate(LancheBase):
    pass

class LancheOut(LancheBase):
    id_lanche: int

    class Config:
        orm_mode = True

class PedidoBase(BaseModel):
    id_usuario: int
    valor_total: float
    forma_pagamento: str
    status: Optional[str] = "pendente"
    data_pedido: Optional[datetime]

class PedidoCreate(PedidoBase):
    pass

class PedidoOut(PedidoBase):
    id_pedido: int

    class Config:
        orm_mode = True

class ItemPedidoBase(BaseModel):
    id_pedido: int
    id_lanche: int
    quantidade: int

class ItemPedidoCreate(ItemPedidoBase):
    pass

class ItemPedidoOut(ItemPedidoBase):
    id_item: int

    class Config:
        orm_mode = True

class CardapioDoDiaBase(BaseModel):
    data: date
    id_lanche: int
    disponivel: Optional[bool] = True
    observacao: Optional[str]

class CardapioDoDiaCreate(CardapioDoDiaBase):
    pass

class CardapioDoDiaOut(CardapioDoDiaBase):
    id_cardapio: int

    class Config:
        orm_mode = True
class PagamentoCreate(BaseModel):
    id_pedido: int
    status_pagamento: str
    metodo_pagamento: str
    valor_pago: float
    data_pagamento: Optional[datetime] = None
    transacao_externa_id: Optional[str] = None

class PagamentoOut(PagamentoCreate):
    id_pagamento: int