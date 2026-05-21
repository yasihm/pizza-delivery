from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Pizza
from dependencies import pegar_sessao, verificar_token
from schemas import PizzaSchema

router = APIRouter(prefix="/pizzas", tags=["pizzas"])

# Listar cardápio (público)
@router.get("/cardapio")
async def listar_cardapio(db: AsyncSession = Depends(pegar_sessao)):
    result = await db.execute(
        select(Pizza).where(Pizza.disponivel == True)
    )
    pizzas = result.scalars().all()
    return {"pizzas": pizzas}

# Listar todas (admin)
@router.get("/admin/todas")
async def listar_todas_pizzas(
    usuario: Usuario = Depends(verificar_token),
    db: AsyncSession = Depends(pegar_sessao)
):
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Requer admin.")
    
    result = await db.execute(select(Pizza))
    pizzas = result.scalars().all()
    return {"pizzas": pizzas}

# Criar pizza (admin)
@router.post("/admin/criar")
async def criar_pizza(
    pizza_schema: PizzaSchema,
    usuario: Usuario = Depends(verificar_token),
    db: AsyncSession = Depends(pegar_sessao)
):
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Requer admin.")
    
    nova_pizza = Pizza(
        nome=pizza_schema.nome,
        preco=pizza_schema.preco,
        descricao=pizza_schema.descricao,
        imagem=pizza_schema.imagem,
        disponivel=pizza_schema.disponivel
    )
    
    db.add(nova_pizza)
    await db.commit()
    await db.refresh(nova_pizza)
    
    return {"mensagem": f"Pizza {nova_pizza.nome} criada com sucesso", "pizza": nova_pizza}

# Atualizar pizza (admin)
@router.put("/admin/atualizar/{pizza_id}")
async def atualizar_pizza(
    pizza_id: int,
    pizza_schema: PizzaSchema,
    usuario: Usuario = Depends(verificar_token),
    db: AsyncSession = Depends(pegar_sessao)
):
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Requer admin.")
    
    result = await db.execute(select(Pizza).where(Pizza.id == pizza_id))
    pizza = result.scalar_one_or_none()
    
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza não encontrada")
    
    pizza.nome = pizza_schema.nome
    pizza.preco = pizza_schema.preco
    pizza.descricao = pizza_schema.descricao
    pizza.imagem = pizza_schema.imagem
    pizza.disponivel = pizza_schema.disponivel
    
    await db.commit()
    
    return {"mensagem": f"Pizza {pizza.nome} atualizada com sucesso"}

# Deletar pizza (admin)
@router.delete("/admin/deletar/{pizza_id}")
async def deletar_pizza(
    pizza_id: int,
    usuario: Usuario = Depends(verificar_token),
    db: AsyncSession = Depends(pegar_sessao)
):
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Requer admin.")
    
    result = await db.execute(select(Pizza).where(Pizza.id == pizza_id))
    pizza = result.scalar_one_or_none()
    
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza não encontrada")
    
    await db.delete(pizza)
    await db.commit()
    
    return {"mensagem": f"Pizza {pizza.nome} deletada com sucesso"}