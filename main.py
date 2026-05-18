from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
import bcrypt  

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES =int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Codificar uma senha
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

def hash_password(senha: str) -> str:
    return bcrypt_context.hash(senha)

#Verificar uma senha
def verify_password(senha: str, hash: str) -> bool:
    return bcrypt_context.verify(senha, hash)



app = FastAPI()

#importar depois de FastAPI
from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)



# para rodar o nosso código, executar no terminal: uvicorn main:app --reload ou \.venv\Scripts\uvicorn.exe main:app --reload 