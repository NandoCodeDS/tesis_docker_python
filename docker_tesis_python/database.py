import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="mnpe"
    )

def cerrar_conexion(conexion):
    conexion.close()