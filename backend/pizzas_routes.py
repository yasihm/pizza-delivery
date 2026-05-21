from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models import Pizza

router = APIRouter()

@router.get("/cardapio")
def get_cardapio(db: Session = Depends(get_db)):
    pizzas = db.query