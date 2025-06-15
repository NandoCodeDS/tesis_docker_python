from .database import conectar, cerrar_conexion

def crear_registro(datos):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO monitor (
                voltaje, frecuencia, va, vb, vc,
                ia, ib, ic, pa, pb, pc,
                qa, qb, qc, sa, sb, sc,
                pfa, pfb, pfc, f, phia, phib, phic
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(consulta, datos)
        conexion.commit()
    except Exception as e:
        print(f"Error al insertar: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        cerrar_conexion(conexion)
