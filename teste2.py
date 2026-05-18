from models import db, Usuario
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db)
session = Session()

usuarios = session.query(Usuario).all()
for u in usuarios:
    print(f"id: {u.id} | admin: {u.admin} | tipo: {type(u.admin)}")