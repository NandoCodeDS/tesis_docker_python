from .database import conectar, cerrar_conexion

def crear_registro(datos):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO monitor (
                voltaje, frecuencia
            ) VALUES (%s, %s)
        """
        cursor.execute(consulta, datos)
        conexion.commit()
    except Exception as e:
        print(f"Error al insertar: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        cerrar_conexion(conexion)
        
from sqlalchemy import Column, String
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario = Column(String(50), primary_key=True, index=True)
    contraseña = Column(String(100))

        
