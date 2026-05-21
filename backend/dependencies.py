from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from database import get_db
from models import Usuario
from security import SECRET_KEY, ALGORITHM

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login-form")

async def pegar_sessao() -> AsyncSession:
    async for session in get_db():
        yield session

async def verificar_token(token: str = Depends(oauth2_schema), db: AsyncSession = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(dic_info.get("sub"))
        result = await db.execute(select(Usuario).where(Usuario.id == id_usuario))
        usuario = result.scalar_one_or_none()
        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        return usuario
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")