from fastapi import HTTPException
from pydantic import BaseModel
from .database import conectar, cerrar_conexion

class Usuario(BaseModel):
    usuario: str
    contraseña: str

def login(usuario: Usuario):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND contraseña=%s", 
                       (usuario.usuario, usuario.contraseña))
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
