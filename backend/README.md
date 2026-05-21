# 🍕 Pizza Delivery API

A REST API for managing pizza delivery orders, built with FastAPI and SQLAlchemy.

## 🚀 Technologies

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Uvicorn](https://www.uvicorn.org/)

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/seu-usuario/pizza-delivery.git
cd pizza-delivery

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head
```

## ▶️ Running

```bash
uvicorn main:app --reload
```

Access the interactive docs at: http://127.0.0.1:8000/docs

## �endpoints Endpoints

### Auth
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Login and get token |

### Orders
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/pedidos/` | Default orders route |
| POST | `/pedidos/pedido` | Create a new order |
| GET | `/pedidos/listar` | List all orders (admin) |
| GET | `/pedidos/listar/pedidos-usuario` | List orders by logged user |
| POST | `/pedidos/pedido/cancelar/{id}` | Cancel an order |
| POST | `/pedidos/pedido/adicionar-item/{id}` | Add item to order |
| POST | `/pedidos/pedido/remover-item/{id}` | Remove item from order |

## 🔐 Authentication

This API uses **Bearer Token** (JWT). After login, include the token in the header:

```
Authorization: Bearer <your_token>
```