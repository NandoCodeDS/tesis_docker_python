# En usuarios.py
from fastapi import APIRouter, HTTPException
from .database import conectar, cerrar_conexion

router = APIRouter()

    
def log(usuario):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario.usuario))
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

