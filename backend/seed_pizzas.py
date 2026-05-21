import asyncio
from database import AsyncSessionLocal
from models import Pizza

async def seed_pizzas():
    async with AsyncSessionLocal() as session:
        pizzas = [
            Pizza(nome="Margherita", preco=35.90, descricao="Molho de tomate, mussarela, manjericão"),
            Pizza(nome="Pepperoni", preco=45.90, descricao="Molho de tomate, mussarela, pepperoni"),
            Pizza(nome="Portuguesa", preco=49.90, descricao="Molho de tomate, mussarela, presunto, ovo, cebola"),
            Pizza(nome="Quatro Queijos", preco=52.90, descricao="Mussarela, provolone, parmesão, gorgonzola"),
            Pizza(nome="Calabresa", preco=42.90, descricao="Molho de tomate, mussarela, calabresa, cebola"),
        ]
        
        for pizza in pizzas:
            session.add(pizza)
        
        await session.commit()
        print(f"{len(pizzas)} pizzas adicionadas ao cardápio!")

if __name__ == "__main__":
    asyncio.run(seed_pizzas())