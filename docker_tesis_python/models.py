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
        
