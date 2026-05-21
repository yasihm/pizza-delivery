from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",           # desenvolvimento local
        "https://pizza-delivery-frontend.vercel.app"  # produção
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)



# para rodar o nosso código, executar no terminal: uvicorn main:app --reload ou \.venv\Scripts\uvicorn.exe main:app --reload    