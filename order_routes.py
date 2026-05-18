from fastapi import APIRouter,  Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema
from models import Pedido, Usuario

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    """
    Essa é a rota padrão para pedidos.
    """
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)  
):
    novo_pedido = Pedido(usuario=usuario.id)  
    session.add(novo_pedido)
    session.commit()
    session.refresh(novo_pedido)
    return {"mensagem": f"Pedido criado com sucesso. Id do pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido:int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    # usuario.admin = True
    # usuario.id = pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()                     
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    pedido.status= "CANCELADO"
    session.commit()
    return {
        "mensagem" : f"Pedido número: {pedido.id} cancelado com sucesso",
        "pedido" : pedido
    }
    
@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    else: 
        pedidos = session.query(Pedido).all()
        return{
            "pedidos" : pedidos
        }
