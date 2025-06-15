from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .modbus_reader import ConnectionModbusClient
from .usuarios import router as usuarios_router

# 🔌 Iniciar FastAPI antes de usarla
app = FastAPI()

# 🧩 Incluir el router de usuarios
app.include_router(usuarios_router)

# 🔌 Configuración de conexión
DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "52.14.42.244"
DB_PORT = "3307"
DB_NAME = "mnpe"  # ← Corregido: dijiste que la base era "mnpe"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 🎯 Modelo de la base de datos
class Monitor(Base):
    __tablename__ = "monitor"
    fecha = Column(DateTime, primary_key=True)
    voltaje = Column(Float)
    frecuencia = Column(Float)

# 🧾 Esquema para entrada de datos (POST)
class MonitorCreate(BaseModel):
    fecha: datetime
    voltaje: float
    frecuencia: float

@app.get("/")
def root():
    return {"message": "API Modbus funcionando"}

@app.post("/capturar")
def capturar():
    client = ConnectionModbusClient("52.14.42.244", 8000)
    datos = client.take_data_device("nodo1")
    return {"status": "Datos capturados", "datos": datos}

@app.get("/datos")
def leer_datos():
    db = SessionLocal()
    try:
        datos = db.query(Monitor).all()
        return [{"fecha": d.fecha, "voltaje": d.voltaje, "frecuencia": d.frecuencia} for d in datos]
    finally:
        db.close()

@app.post("/insertar")
def insertar_dato(monitor: MonitorCreate):
    db = SessionLocal()
    try:
        nuevo = Monitor(
            fecha=monitor.fecha,
            voltaje=monitor.voltaje,
            frecuencia=monitor.frecuencia
        )
        db.add(nuevo)
        db.commit()
        return {"mensaje": "Dato insertado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al insertar: {e}")
    finally:
        db.close()
