from fastapi import FastAPI
from .modbus_reader import ConnectionModbusClient
from .dbase import SessionLocal, engine
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas

# Dependency: obtiene una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()



@app.get("/")
def root():
    return {"message": "API Modbus funcionando"}

@app.post("/capturar")
def capturar():
    client = ConnectionModbusClient("192.168.91.63", 502)
    datos = client.take_data_device("nodo1")
    return {"status": "Datos capturados", "datos": datos}

@app.get("/usuarios/", response_model=list[schemas.UsuarioOut])
def read_usuarios(db: Session = Depends(get_db)):
    return crud.get_usuarios(db)

@app.get("/usuarios/{usuario}", response_model=schemas.UsuarioOut)
def read_usuario(usuario: str, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@app.post("/usuarios/", response_model=schemas.UsuarioOut)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db, usuario)

@app.put("/usuarios/{usuario}", response_model=schemas.UsuarioOut)
def update_usuario(usuario: str, datos: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = crud.update_usuario(db, usuario, datos)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@app.delete("/usuarios/{usuario}")
def delete_usuario(usuario: str, db: Session = Depends(get_db)):
    db_usuario = crud.delete_usuario(db, usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado"}