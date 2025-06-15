from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .database import conectar, cerrar_conexion

router = APIRouter()

class Usuario(BaseModel):
    usuario: str
    contraseña: str

@router.post("/registro")
def registrar_usuario(data: Usuario):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # Verifica si el usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (data.usuario,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El usuario ya existe")

        # Inserta nuevo usuario
        cursor.execute(
            "INSERT INTO usuarios (usuario, contraseña) VALUES (%s, %s)",
            (data.usuario, data.contraseña)
        )
        conexion.commit()

        return {"mensaje": "Usuario registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        cerrar_conexion(conexion)
