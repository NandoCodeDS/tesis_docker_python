from fastapi import FastAPI
from .modbus_reader import ConnectionModbusClient

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API Modbus funcionando"}

@app.post("/capturar")
def capturar():
    client = ConnectionModbusClient("192.168.91.63", 502)
    datos = client.take_data_device("nodo1")
    return {"status": "Datos capturados", "datos": datos}