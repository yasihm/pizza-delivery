from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Pedido, ItemPedido, Usuario
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema

pedidos_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@pedidos_router.get("/listar/pedidos-usuario")
async def listar_pedidos_usuario(
    usuario: Usuario = Depends(verificar_token),
    session: AsyncSession = Depends(pegar_sessao)
):
    result = await session.execute(
        select(Pedido).where(Pedido.usuario == usuario.id)
    )
    pedidos = result.scalars().all()
    return {"pedidos": pedidos}

@pedidos_router.post("/pedido")
async def criar_pedido(
    usuario: Usuario = Depends(verificar_token),
    session: AsyncSession = Depends(pegar_sessao)
):
    novo_pedido = Pedido(usuario=usuario.id)
    session.add(novo_pedido)
    await session.commit()
    await session.refresh(novo_pedido)
    return {"mensagem": f"Pedido {novo_pedido.id} criado com sucesso"}

@pedidos_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(
    id_pedido: int,
    usuario: Usuario = Depends(verificar_token),
    session: AsyncSession = Depends(pegar_sessao)
):
    result = await session.execute(
        select(Pedido).where(Pedido.id == id_pedido)
    )
    pedido = result.scalar_one_or_none()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if pedido.usuario != usuario.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    pedido.status = "CANCELADO"
    await session.commit()
    return {"mensagem": f"Pedido {pedido.id} cancelado com sucesso"}