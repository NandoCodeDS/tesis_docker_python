# En usuarios.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .database import conectar, cerrar_conexion

router = APIRouter()

class Usuario(BaseModel):
    usuario: str
    contraseña: str

@router.post("/registro")
def registrar(usuario: Usuario):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, contraseña) VALUES (%s, %s)", (usuario.usuario, usuario.contraseña))
        conexion.commit()
        return {"mensaje": "Usuario registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        cerrar_conexion(conexion)

@router.post("/login")
def login(usuario: Usuario):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND contraseña=%s", (usuario.usuario, usuario.contraseña))
        resultado = cursor.fetchone()
        if resultado:
            return {"mensaje": "Login exitoso"}
        else:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'cursor' in locals():
            cursor.close()
        cerrar_conexion(conexion)
